from icecube import icetray, dataio, simclasses, dataclasses
from icecube.icetray import I3Tray
import click, time

# This script filters event frames in an I3 file and keep frames that contain DiMuon Events.
# This was specifically used for L2, but should work for others.

@click.command()
@click.option('--infile',  '-i', required=True, help='Infile name')
@click.option('--outfile', '-o', required=True, help='Outfile name')
def main(infile, outfile):
    start_time = time.time()

    tray = I3Tray()
    tray.AddModule("I3Reader", "reader", Filename=infile)

    def filter_dimuon(frame):
        if frame.Stop != icetray.I3Frame.Physics:
            return True
        # if 'CVStatistics' in frame:
        #     return False
        if 'I3MCTree' not in frame:
            return False

        tree = frame["I3MCTree"]
        head = tree.get_head()
        children = tree.children(head)
        if not children:
            return False
        pdg = children[0].pdg_encoding
        energy = children[0].energy

        if abs(pdg) == 13:
            for d in children:
                if abs(d.pdg_encoding) in (411, 421):
                    for d_child in tree.children(d):
                        if abs(d_child.pdg_encoding) == 13 and d_child.energy > 0 and energy > 0:
                            return True
        return False

    tray.AddModule(filter_dimuon, "frame_filter")

    tray.AddModule("I3OrphanQDropper", "dropper")
    tray.AddModule("I3Writer", "writer", Filename=outfile)
    tray.Execute()
    tray.Finish()
    print(f"Done! Time elapsed {time.time() - start_time:.2f} seconds.")

if __name__ == '__main__':
    main()