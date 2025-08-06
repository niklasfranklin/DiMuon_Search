import sys
import time
import os
import glob
import click
import numpy as np
import yaml

from icecube import icetray, dataio, dataclasses, hdfwriter, phys_services
from icecube.icetray import I3Tray

from meows.legacy_modules.add_meows_bdt import ApplyMEOWSBDT
from meows.legacy_modules.add_leptonweighter_variables import AddLeptonWeighterVariables

from ic3_labels.labels.modules import MCLabelsCascades
from meows.legacy_modules.get_weighted_primary import get_weighted_primary
from meows.legacy_modules.recreate_and_add_mmc_tracklist import RerunProposal
from meows.legacy_modules.add_meows_xlevel import add_meows_xlevel, XLEVEL_KEYS

@icetray.traysegment
def ApplyBDTCuts(tray, name, bdt_cut):
    """
    Applies the following cuts:
    500 GeV < E_reco < 100 TeV
    costhz < 0.0
    BDT > bdt_cut
    """
    def apply_cuts(frame):
        if ((frame['energy_reco_new_I3Particle'].energy > 5e2) & \
            (frame['energy_reco_new_I3Particle'].energy < 1e5) & \
            (np.cos(frame['MuEx'].dir.zenith) < 0.0)): #& \
        #     (frame['BDT'].value > bdt_cut)): #& \
        #     #(frame['DeepStart'].value > 0.99)):
          
            return True
        # if (frame['BDT'].value > bdt_cut):
        #     return True
        
        return False
    
    tray.Add(apply_cuts)

def rename_mctree(frame, mctree_name='I3MCTree'):
    frame[mctree_name+'_preMuonProp'] = dataclasses.I3MCTree(frame[mctree_name])
    del frame[mctree_name]

def add_labels(frame):
    # if not frame.Has('LabelsDeepLearning'):  # TODO: The name of the labels should be an input
    #     tray.Add(rename_mctree)
    #     tray.AddSegment(RerunProposal, 'RerunProposal')  # TODO: Is this even working?
    #     tray.AddModule(get_weighted_primary, 'getWeightedPrimary',
    #                    If=lambda f: not f.Has('MCPrimary'))
    #     tray.AddModule(MCLabelsCascades,
    #                   'MCLabelsCascades',
    #                   PulseMapString='InIceDSTPulses',
    #                   PrimaryKey='MCPrimary',
    #                   ExtendBoundary=[0],
    #                   OutputKey='LabelsDeepLearning')
    
    dnn_reco_labels = frame['LabelsDeepLearning']
    
    frame.Put('EnergyVisible', dataclasses.I3Double(dnn_reco_labels['EnergyVisible']))    
    frame.Put('InelasticityVisible', dataclasses.I3Double(dnn_reco_labels['InelasticityVisible']))
    frame.Put('TrackEnergy', dataclasses.I3Double(dnn_reco_labels['TrackEnergy']))    
    frame.Put('HadronEnergy', dataclasses.I3Double(dnn_reco_labels['HadronEnergy']))
    frame.Put('TotalDepositedEnergy', dataclasses.I3Double(dnn_reco_labels['TotalDepositedEnergy']))
    if 'Qsq' in dnn_reco_labels.keys():  # Not all files may have this
        frame.Put('Qsq', dataclasses.I3Double(dnn_reco_labels['Qsq']))

@icetray.traysegment
def AddDNNLabels(tray, name):
    # tray.Add(rename_mctree)
    # tray.AddSegment(RerunProposal, 'RerunProposal')  # TODO: Is this even working?
    tray.AddModule(get_weighted_primary, 'getWeightedPrimary',
                    If=lambda f: not f.Has('MCPrimary'))
    tray.AddModule(MCLabelsCascades,
                  'MCLabelsCascades',
                  PulseMapString='InIceDSTPulses',
                  PrimaryKey='MCPrimary',
                  ExtendBoundary=0,
                  OutputKey='LabelsDeepLearning')
    tray.AddModule(MCLabelsCascades,
                  'MCLabelsCascades_p150',
                  PulseMapString='InIceDSTPulses',
                  PrimaryKey='MCPrimary',
                  ExtendBoundary=150,
                  OutputKey='LabelsDeepLearning_p150')
    tray.Add(add_labels)
    
@click.command()
@click.option('--infile', '-i', default='/n/holyscratch01/arguelles_delgado_lab/Everyone/pweigel/test3_MEOWS_DNN.i3.zst', help='Infile')
@click.option('--outfile', '-o', default='/n/holyscratch01/arguelles_delgado_lab/Everyone/pweigel/test3_MEOWS_BDT.i3.zst', help='Outfile')
@click.option('--config', '-c', help='Configuration file')
@click.option('--debug', default=False, type=bool, is_flag=True, help='Enable debug info')
def main(infile, outfile, config, debug):
  
    # New config settings
    cfg = yaml.safe_load(open(config))['BDT']
  
    if 'gcdfile' in cfg.keys() and cfg['gcdfile'] is not None:
        infiles = [cfg['gcdfile'], infile]
        print('GCD being used here: {}'.format(cfg['gcdfile']))
    else:
        infiles = [infile]
        print('No GCD file found in configuration.')

    start_time = time.time()
    tray = I3Tray()

    # read in files
    tray.AddModule("I3Reader", "reader", Filenamelist=infiles)
    
    # Get rid of NullSplits, they're annoying
    def remove_frame(frame, stream_name):
        if 'I3EventHeader' in frame:
            if frame['I3EventHeader'].sub_event_stream == stream_name:
                return False
        return True
    
    if ('drop_nullsplit' in cfg and cfg['drop_nullsplit']):
        tray.AddModule(remove_frame, "DeleteSubstream", stream_name='NullSplit')
        
    # Get LW variables
    if ('add_lw' in cfg and cfg['add_lw']):
        # Make sure all the required settings are specified
        if (cfg['lic_location'] is not None):
            tray.AddSegment(AddLeptonWeighterVariables, "LW_vars", lic=cfg['lic_location'], xs_location=cfg['xs_location'])
    else:
        print('Not adding LW variables!')

    # tray.AddSegment(ApplyMEOWSBDT, "MEOWS_BDT",
    #                 bdt_weights_path=cfg['weights_path'],
    #                 output_key=cfg['output_key'])
    
    if ('apply_cut' in cfg and cfg['apply_cut']):
        if cfg['bdt_cut'] != 0.83:  # Warn if the cut value is not the standard MEOWS one
            print('Warning: BDT cut value is not 0.83, it is: {}!'.format(cfg['bdt_cut']))
        tray.AddSegment(ApplyBDTCuts, "BDTcuts",
                        bdt_cut=cfg['bdt_cut'])
        
    if ('add_dnn_labels' in cfg and cfg['add_dnn_labels']):
        tray.AddSegment(AddDNNLabels, 'AddDNNLabels')

    # Quick fix for the mislabeled transformer reco, effects some of the systematic sets
    if ('rename_transformer_reco' in cfg and cfg['rename_transformer_reco']):
        def rename_transformer_reco(frame):
            if frame.Has('TransformerReco_inelasticity_test'):
                frame['TransformerReco_inelasticity'] = frame['TransformerReco_inelasticity_test']
        tray.Add(rename_transformer_reco)
        
    # Add the MEOWS XLevel variables if needed
    if ('add_meows_xlevel' in cfg and cfg['add_meows_xlevel']):
        tray.Add(add_meows_xlevel)

    if ('write_i3' in cfg and cfg['write_i3']):
        tray.Add("I3OrphanQDropper")
        # NOTE: we do not save the GCD here to save space!
        tray.AddModule("I3Writer", "EventWriter", filename=outfile, Streams=[icetray.I3Frame.DAQ, icetray.I3Frame.Physics])
        
    if ('write_h5' in cfg and cfg['write_h5']):        
        # These keys are ones that are NEEDED for the MEOWS sample! You can add more with 'keep_keys' in the config.
        classification_keys = ['DeepStart', 'DeepCascade', 'DeepSkim', 'DeepStop', 'DeepThrough', 'BDT']
        mc_truth_keys = ['FinalType0', 'FinalType1', 'FinalStateX', 'FinalStateY',
                         'NuEnergy', 'NuZenith', 'NuAzimuth', 'PrimaryType', 'oneweight', 'weights']
        multisim_keys = ['MultisimAmplitudes', 'MultisimPhases']
        reconstruction_keys = ['DnnEnergy', 'MuExAzimuth', 'MuExZenith', 'MuExEnergy', 'CorrectedParaboloidSigma', 'I3EventHeader']

        keep_keys = classification_keys + mc_truth_keys + multisim_keys + reconstruction_keys
        if ('keep_keys' in cfg):
            keep_keys += cfg['keep_keys']

        if ('add_dnn_labels' in cfg and cfg['add_dnn_labels']):
            keep_keys += ['EnergyVisible', 'InelasticityVisible', 'TrackEnergy', 'HadronEnergy', 'Qsq', 'TotalDepositedEnergy',
                          'LabelsDeepLearning', 'LabelsDeepLearning_p150']
        if ('write_xlevel_keys' in cfg and cfg['write_xlevel_keys']):
            keep_keys += XLEVEL_KEYS
        
        keep_keys = list(set(keep_keys))  # Make sure each key only appears once
        print("Keys to keep:\n    ", keep_keys)
        
        # outfile will end in .i3.zst, so we need to fix that
        h5_outfile = outfile.split('.i3')[0]+'.h5'
        tray.AddSegment(hdfwriter.I3HDFWriter, 'hdfwriter',
                        Output=h5_outfile,
                        CompressionLevel=9,
                        Keys=keep_keys,
                        SubEventStreams=['in_ice', 'InIceSplit', 'TTrigger', 'Final', 'topological_split'])

    tray.Execute()

    tray.Finish()

    print(time.time()-start_time,"seconds")

if __name__ == "__main__":
    main()