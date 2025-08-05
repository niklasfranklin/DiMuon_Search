#!/bin/sh /cvmfs/icecube.opensciencegrid.org/py3-v4.3.0/icetray-start
#METAPROJECT /data/ana/SterileNeutrino/IC86/HighEnergy/Metaprojects/feline_v1/build/icetray

import sys, os, time
sys.path.insert(0,'/n/holylfs05/LABS/arguelles_delgado_lab/Everyone/nfranklin/repo/MEOWS')
from os.path import expandvars
import click, yaml

import numpy as np
import icecube
from icecube.icetray import I3Tray, I3Units
from icecube import tableio, hdfwriter, icetray, dataclasses, dataio, phys_services, LeptonInjector
from icecube import wavedeform, TopologicalSplitter, WaveCalibrator, VHESelfVeto, CoincSuite, bayesian_priors, mue

print('Loading processing modules... ', end='')

# This should go into some __init__ file... #
import meows.legacy_modules
from meows.legacy_modules.get_pulse_names import get_pulse_names
from meows.legacy_modules.isLowUpOnly import isLowUpOnly
from meows.legacy_modules.isMuonFilter import isMuonFilter
from meows.legacy_modules.overburden import overburden
from meows.legacy_modules.outer_charge import outer_charge
from meows.legacy_modules.is_simulation import is_simulation
from meows.legacy_modules.interaction_type import interaction_type
from meows.legacy_modules.hasTWSRTOfflinePulses import hasTWSRTOfflinePulses
from meows.legacy_modules.getWeightingCandidate import getWeightingCandidate
from meows.legacy_modules.finalNeutrino import finalNeutrino
from meows.legacy_modules.doExpensiveRecos import doExpensiveRecos
from meows.legacy_modules.precut import precut
from meows.legacy_modules.fixWeightMap import fixWeightMap
from meows.legacy_modules.get_cut_variables import get_cut_variables
from meows.legacy_modules.get_pulses import get_pulses
from meows.legacy_modules.add_split_reconstructions import add_split_reconstructions
from meows.legacy_modules.add_bayesian_reconstruction import add_bayesian_reconstruction
from meows.legacy_modules.add_basic_reconstructions import add_basic_reconstructions
from meows.legacy_modules.SamePulseChecker import SamePulseChecker
from meows.legacy_modules.EntryEnergy import EntryEnergy
from meows.legacy_modules.splitFrames import splitFrames
from meows.legacy_modules.basicRecosAlreadyDone import basicRecosAlreadyDone
from meows.legacy_modules.computeSimpleCutVars import computeSimpleCutVars
from meows.legacy_modules.cutL3 import cutL3
from meows.legacy_modules.FindDetectorVolumeIntersections import FindDetectorVolumeIntersections
from meows.legacy_modules.parabaloidCut import parabaloidCut
from meows.legacy_modules.afterpulses import afterpulses
from meows.legacy_modules.add_paraboloid import add_paraboloid
from meows.legacy_modules.planL3Cut import planL3Cut
from meows.legacy_modules.get_variables import get_variables
from meows.legacy_modules.is_cut_time import is_cut_time
from meows.legacy_modules.true_trackfit import true_trackfit
from meows.legacy_modules.goodFit import goodFit
from meows.legacy_modules.findHighChargeDOMs import findHighChargeDOMs
from meows.legacy_modules.renameMCTree import renameMCTree
from meows.legacy_modules.dumbOMSelection import dumbOMSelection
from meows.legacy_modules.controls import outkeys, i3streams, dh_definitions, stConfigService, delkeys, deepCoreStrings
from meows.legacy_modules.ComputeChargeWeightedDist import ComputeChargeWeightedDist
from meows.legacy_modules.final_selection import finalSample
from meows.legacy_modules.packet_cutter import NewPacketCutter
from meows.legacy_modules.paraboloid_sigma_corrector import NewParaboloidSigmaCorrector
from meows.legacy_modules.helper_functions import check_write_permissions, parse_boolean, truecondition
print('Done!')


@click.command()
@click.option('--infile',  '-i', 
              required=True, 
              type=str, 
              help='Infile name')
@click.option('--outfile', '-o', 
              required=True, 
              type=str, 
              help='Outfile name')
@click.option('--gcdfile', '-g', 
              required=True, 
              type=str, 
              help='GCD file')
@click.option('--ice_model',
              default='spice_3.2',
              type=str,
              help='Ice model name')
@click.option('--spline_path',
              default='../resources/paraboloidCorrectionSpline.dat',
              type=str,
              help='ParaboloidSigma spline path')
@click.option('--nframes', '-n', 
              default=-1, 
              type=int, 
              help='Number of frame to process')
@click.option('--debug', 
              default=False, 
              type=bool, is_flag=True, 
              help='Enable debug info')
def main(infile, outfile, gcdfile, ice_model, spline_path, nframes, debug):    
    start_time = time.time()
         
    ice_model_location = expandvars("$I3_BUILD/ice-models/resources/models/ICEMODEL/"+ice_model)
    infiles = [gcdfile, infile]
    
    InIcePulses, SRTInIcePulses, SRTInIcePulses_NoDC_Qtot, SRTInIcePulses_NoDC = get_pulse_names(infile)

    tray = I3Tray()
    tray.AddService("I3GSLRandomServiceFactory", "Random") # needed for bootstrapping
    tray.AddModule("I3Reader", "reader", FilenameList=infiles)

    # I3MCTree_preMuonProp --> I3MCTree
    tray.AddModule(renameMCTree, "_renameMCTree", Streams=[icetray.I3Frame.DAQ])

    # Remove all events that don't pass muon filter
    tray.AddModule(isMuonFilter & hasTWSRTOfflinePulses,"selectValidData")

    # Make sure all expected values are in CorsikaWeightMap
    tray.AddModule(fixWeightMap, "patchCorsikaWeights")

    # Remove DeepCore strings from PulseMap
    tray.AddModule(dumbOMSelection,"NoDeepCore",
                   pulses         = SRTInIcePulses,
                   output         = SRTInIcePulses_NoDC,
                   omittedStrings = deepCoreStrings,
                   IfCond         = truecondition)

    tray.AddModule(ComputeChargeWeightedDist, "CCWD", Pulses=SRTInIcePulses_NoDC, Track="PoleMPEFitName")

    # Perform initial data reduction cut
    tray.AddModule(precut, "ApplyPrecuts")

    # Remove QFrames from things which got cut
    tray.AddModule("I3OrphanQDropper", "OrphanQDropper")

    tray.AddModule("I3SeededRTCleaning_RecoPulse_Module", "SRTClean",
                   InputHitSeriesMapName  = InIcePulses,
                   OutputHitSeriesMapName = SRTInIcePulses,
                   STConfigService        = stConfigService,
                   #SeedProcedure         = "HLCCoreHits",
                   NHitsThreshold         = 2,
                   Streams                = [icetray.I3Frame.DAQ])
    
    tray.AddModule("I3TopologicalSplitter", "TTrigger",
                   SubEventStreamName = "TTrigger", #Spencer -- Is this ok?? I was getting warnigngs... Jeff: Is it ?
                   InputName          = SRTInIcePulses,
                   OutputName         = "TTPulses",
                   Multiplicity       = 4,
                   TimeWindow         = 4000*I3Units.ns,
                   TimeCone           = 800*I3Units.ns,
                   SaveSplitCount     = True)

    tray.AddModule(lambda f: f.Put("TTriggerReducedCount", icetray.I3Int(0)), "ReducedCountMaker", Streams = [icetray.I3Frame.DAQ])
    tray.AddModule("AfterpulseDiscard", "DiscardAfterpulses",
                   SplitName="TTrigger",
                   RecoMapName="TTPulses",
                   QTotFraction=0.1,
                   TimeOffSet=3e3*I3Units.ns,
                   OverlapFraction=0.75,
                   Discard=True)

    tray.AddModule(SamePulseChecker, "SPC")
    add_basic_reconstructions(tray,"_TT", "TTPulses", splitFrames & ~basicRecosAlreadyDone)
    computeSimpleCutVars(tray, splitFrames)
    add_bayesian_reconstruction(tray, "TTPulses", splitFrames & doExpensiveRecos, "TrackFit")
    add_paraboloid(tray, "TTPulses", splitFrames & doExpensiveRecos, "TrackFit")
    add_split_reconstructions(tray, "TTPulses", splitFrames & doExpensiveRecos, "TrackFit")

    tray.AddModule(NewParaboloidSigmaCorrector, "newExtractSigma",
                   CorrectionSplinePath=spline_path,
                   ParaboloidParameters="TrackFitParaboloidFitParams",
                   NChanSource="NChanSource",
                   Output="CorrectedParaboloidSigma")

    tray.AddModule(planL3Cut,"CutPlanner")

    tray.AddModule("I3WaveformTimeRangeCalculator", "WaveformRange", If=lambda frame: not 'CalibratedWaveformRange' in frame)
    tray.AddModule(wavedeform.AddMissingTimeWindow, "PulseTimeRange")
    tray.AddModule(findHighChargeDOMs, "findHighChargeDOMs",
                   pulses = InIcePulses,
                   outputList = "BrightDOMs")

    tray.AddModule("muex", "muex",
                   pulses='TTPulses', #MuEx does not handle noise, so it should run on cleaned pulses
                   rectrk='TrackFit',
                   result='MuEx',
                   lcspan=0,
                   repeat=0,
                   rectyp=True,
                   usempe=False,
                   detail=False,
                   energy=True,
                   compat=False, #New Addition bug fix
                   icedir=ice_model_location,
                   If=finalSample)

    tray.Add(true_trackfit)
    tray.AddModule("FiducialVolumeEntryPointFinder", "findEntryPoints",
                   TopBoundaryWidth=0.,
                   BottomBoundaryWidth=0.,
                   SideBoundaryWidth=0.,
                   AssumeMuonTracksAreInfinite=True,
                   ParticleIntersectionsName="IntersectingParticles",
                   If=is_simulation)
    
    tray.AddModule(FindDetectorVolumeIntersections, "FindDetectorVolumeIntersections",
                   TimePadding = 60.*I3Units.m/dataclasses.I3Constants.c,
                   TrackName="TrackFit",
                   OutputTimeWindow="ContainedTimeRange")
    
    tray.AddModule(EntryEnergy, "EntryEnergy")
    tray.AddModule(finalNeutrino, "finalNeutrino")
    #tray.AddModule(interaction_type, 'InteractionType', infile=infile)
    tray.Add(overburden)
    tray.Add(outer_charge)
    tray.Add(get_cut_variables)
    tray.Add(get_pulses)
    
    tray.AddModule(getWeightingCandidate, "weightingcand")
    finalWithParab = finalSample & parabaloidCut
    tray.AddModule(finalWithParab, "finalSample")
    
    tray.AddModule('Delete', 'delkeys', Keys = delkeys)

    tray.AddModule(NewPacketCutter, "NewCutter",
                   CutStream="TTrigger",
                   CutObject="CutL3")

    tray.AddModule("I3Writer", "i3writer",
                   Filename=outfile,
                   Streams=i3streams)

    if nframes >= 0:
        tray.Execute(nframes)
    else:
        tray.Execute()

    tray.Finish()
    
    print('Done! Time elapsed {:.2f} seconds.'.format(time.time() - start_time))
    
main()