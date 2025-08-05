import sys, time, os, glob
import click
import numpy as np
import yaml

from icecube import icetray, dataio, dataclasses, phys_services
from icecube.icetray import I3Tray

try:
    from dnn_reco.ic3.segments import ApplyDNNRecos
except ImportError:
    print('Could not import dnn_reco, make sure it is installed!')

def build_egen_seed(frame, output_key='event_selection_egen_seed', 
                    pos_name='pos_01', dir_name='dir_01', energy_name='energy_01', time_name='time_01'):
    prefix = 'DeepLearningReco_event_selection_egen_seed_'
    new_particle = dataclasses.I3Particle()

    new_particle.pos.x = frame[prefix + pos_name+'_I3Particle'].pos.x
    new_particle.pos.y = frame[prefix + pos_name+'_I3Particle'].pos.y
    new_particle.pos.z = frame[prefix + pos_name+'_I3Particle'].pos.z
    new_particle.dir = frame[prefix + dir_name+'_I3Particle'].dir
    new_particle.time = frame[prefix + time_name+'_I3Particle'].time
    new_particle.energy = frame[prefix + energy_name+'_I3Particle'].energy
    
    new_particle.fit_status = dataclasses.I3Particle.FitStatus.OK
    new_particle.shape = getattr(dataclasses.I3Particle.ParticleShape, 'Cascade')  # For now
    
    frame[output_key] = new_particle

def build_cascade(frame):
    cascade_vertex = dataclasses.I3MapStringDouble()
    cascade_vertex['VertexX'] = frame['DeepLearningReco_event_selection_egen_seed_pos_01']['VertexX']
    cascade_vertex['VertexY'] = frame['DeepLearningReco_event_selection_egen_seed_pos_01']['VertexY']
    cascade_vertex['VertexZ'] = frame['DeepLearningReco_event_selection_egen_seed_pos_01']['VertexZ']
    cascade_vertex['VertexTime'] = frame['DeepLearningReco_event_selection_egen_seed_time_01']['VertexTime']
    cascade_vertex['VertexX_unc'] = frame['DeepLearningReco_event_selection_egen_seed_pos_01']['VertexX_uncertainty']
    cascade_vertex['VertexY_unc'] = frame['DeepLearningReco_event_selection_egen_seed_pos_01']['VertexY_uncertainty']
    cascade_vertex['VertexZ_unc'] = frame['DeepLearningReco_event_selection_egen_seed_pos_01']['VertexZ_uncertainty']
    cascade_vertex['VertexTime_unc'] = frame['DeepLearningReco_event_selection_egen_seed_time_01']['VertexTime_uncertainty']

    frame['cascade_vertex'] = cascade_vertex
    
@click.command()
@click.option('--config',  '-c', required=True, type=str, help='Configuration file')
@click.option('--infile',  '-i', required=True, type=str, help='Infile name')
@click.option('--outfile', '-o', required=True, type=str, help='Outfile name')
@click.option('--nframes', '-n', default=-1, type=int, help='Number of frame to process')
@click.option('--debug', default=False, type=bool, is_flag=True, help='Enable debug info')
def main(config, infile, outfile, nframes, debug):
    # TODO: This script should also remove the garbarge keys -PW
    start_time = time.time() 
    
    cfg = yaml.safe_load(open(config))['DNN']
    
    print(cfg.keys())
    if 'gcdfile' in cfg.keys():
        infiles = [cfg['gcdfile'], infile]
    else:
        print('GCD file not specified!')
        infiles = [infile]

    start_time = time.time()
    tray = I3Tray()
    
    if ('use_gpu' in cfg and cfg['use_gpu']):
        cnn_batch_size = 128
    else:
        cnn_batch_size = 1
        
    cascade_built = False  # Keep track of whether or not we made the cascade yet

    # read in files
    tray.AddModule("I3Reader", "reader", Filenamelist=infiles)
    
    # Get rid of NullSplits, they're annoying
    def remove_frame(frame, stream_name):
        if 'I3EventHeader' in frame:
            if frame['I3EventHeader'].sub_event_stream == stream_name:
                return False
        return True
    
    if cfg['drop_nullsplit']:
        tray.AddModule(remove_frame, "DeleteSubstream", stream_name='NullSplit')
        tray.Add("I3OrphanQDropper")
        
    # if cfg['build_cascade']:
    #     tray.Add(build_cascade)
    
    # Add a segment for each dnn_reco model specified
    if cfg['add_dnn_reco']:
        for model_name, model_options in cfg['dnn_reco_models'].items():
          
            # Check if this model uses cascade_vertex, and if so, build it
            # Remember, the DNNs needed to make the vertex MUST come before this
            # reco in the list!
            if 'cascade_key' in model_options.keys():# and not cascade_built:
                tray.Add(build_cascade)  # TODO: Currently assumes the key is 'cascade_vertex' -PW
          
                tray.AddSegment(ApplyDNNRecos, 'dnn_reco_'+model_name,
                                pulse_key=model_options['pulse_key'],
                                dom_exclusions=model_options['dom_exclusions'],
                                partial_exclusion=True,
                                model_names=[model_name],
                                models_dir=cfg['dnn_reco_models_dir'],
                                output_keys=[model_options['output_key']],
                                batch_size=cnn_batch_size, #when running in gpu
                                num_cpus=cfg['cpu_cores'], #when running in cpu
                                cascade_key=model_options['cascade_key'],
                                )
            else:  # Don't use cascade_key if we don't use it
                tray.AddSegment(ApplyDNNRecos, 'dnn_reco_'+model_name,
                                pulse_key=model_options['pulse_key'],
                                dom_exclusions=model_options['dom_exclusions'],
                                partial_exclusion=True,
                                model_names=[model_name],
                                models_dir=cfg['dnn_reco_models_dir'],
                                output_keys=[model_options['output_key']],
                                batch_size=cnn_batch_size, #when running in gpu
                                num_cpus=cfg['cpu_cores'], #when running in cpu
                                )
    
    if cfg['add_transformer_reco']:
        from nunet.modules.transformer_reco import TransformerReconstruction

        for model_name, model_options in cfg['transformer_models'].items():
            tray.AddModule(TransformerReconstruction, "TransformerReco",
                           ModelConfiguration=model_options['model_config'],
                           PulseMap=model_options['pulse_key'],
                           ModelPath=model_options['model_path'],
                           OutputKey=model_options['output_key'],
                           UseGPU=model_options['use_gpu'],
                           BatchSize=model_options['batch_size'],
                           ConfigOverride=model_options['config_override'],
                           Verbose=False)
        
    if cfg['build_event_generator_seed']:
        tray.Add(build_egen_seed)
    
    # Apply event-generator models
    if cfg['add_event_generator']:
        from egenerator.ic3.segments import ApplyEventGeneratorReconstruction
        for model_name, model_options in cfg['event_generator_models'].items():
            tray.AddSegment(
                ApplyEventGeneratorReconstruction, 'ApplyEventGeneratorReconstruction',
                pulse_key=model_options['pulse_key'],
                dom_and_tw_exclusions=['BadDomsList', 'CalibrationErrata', 'SaturationWindows'],
                partial_exclusion=True,
                exclude_bright_doms=True,
                model_names=[model_name],
                seed_keys=['event_selection_egen_seed'],
                output_key='egenerator_cascade',
                model_base_dir=cfg['event_generator_models_dir'],
                scipy_optimizer_settings={
                    'options': {'gtol': 10},
                },
                num_threads=10,
            )
    
    # i3deepice classification
    if cfg['add_classifier']:
        from i3deepice.i3module_tf2 import DeepLearningModule
        classifier_options = cfg['classifier']
        tray.AddModule(DeepLearningModule, "i3deepice_classifier",
                       pulsemap=classifier_options['pulse_key'],
                       saturation_windows=['SaturationWindows'],
                       bright_doms=['BrightDOMs'],
                       batch_size=cnn_batch_size,
                       cpu_cores=cfg['cpu_cores'],
                       gpu_cores=1,
                       add_truth=False,  
                       model='classification',
                       save_as=classifier_options['output_key'])

    tray.AddModule("I3Writer", "EventWriter", filename=outfile)

    if nframes >= 0:
        tray.Execute(nframes)
    else:
        tray.Execute()

    tray.Finish()
    
    print('Done! Time elapsed {:.2f} seconds.'.format(time.time() - start_time))

if __name__ == "__main__":
    main()
