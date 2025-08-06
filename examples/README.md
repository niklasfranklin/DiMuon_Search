# examples

These scripts are examples of processing an I3File through the desired filters. Each contains an example file
and should return another file as a result. The supplied shell scripts are what send the
jobs to a remote machine for computing.

Optionally, you can run these jobs natively by pasting the lines begininning with 'python' into the command line, 
although the process-DNN scipt makes heavy use of the cpu for processing so keep that in mind.

## filter_Dimuon:

This script inputs an I3file and filters through the event frames so that only frames containing DiMuon events are left over.
I tested it with L2 but I think any other script should work.

## process-XLevel:

The script for processing I3 files from L2 to XLevel (L3)

## process-DNN:

The script for processing XLevel I3 files through DNN Reconstruction.

## process-BDT:

The script for processing XLevel I3 files through DNN Reconstruction.
