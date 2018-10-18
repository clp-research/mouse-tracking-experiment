#!/usr/bin/python

# Copyright (c) 2011-2016 CereProc Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

# make shure cerevoice_eng and Voice folders are in the same directory!

import os
import sys

dir = os.path.dirname(os.path.realpath(__file__))
engdir = os.path.join(dir, 'cerevoice_eng')
sys.path.append(engdir)

import cerevoice_eng

def synth(input_str, filename="output.wav", outdir=None):

    if not outdir:
        cwd = os.getcwd()
        outdir = cwd
    licensefile = os.path.dirname(os.path.abspath(__file__))+"/voice/heather.lic"
    voicefile =os.path.dirname(os.path.abspath(__file__))+ "/voice/cerevoice_heather_4.0.0_48k.voice"
    ondisk = False

    # Create an engine
    engine = cerevoice_eng.CPRCEN_engine_new()

    # Set the loading mode - all data to RAM or with audio and indexes on disk
    loadmode = cerevoice_eng.CPRC_VOICE_LOAD
    if ondisk:
        loadmode = cerevoice_eng.CPRC_VOICE_LOAD_EMB

    # Load the voice
    ret = cerevoice_eng.CPRCEN_engine_load_voice(engine, licensefile, "", voicefile, loadmode)
    if not ret:
        sys.stderr.write("ERROR: could not load the voice, check license integrity\n")
        sys.exit(1)

    # Get some information about the first loaded voice (index 0)
    name = cerevoice_eng.CPRCEN_engine_get_voice_info(engine, 0, "VOICE_NAME");
    srate = cerevoice_eng.CPRCEN_engine_get_voice_info(engine, 0, "SAMPLE_RATE");
    #sys.stderr.write("INFO: voice name is '%s', sample rate '%s'\n" % (name, srate))

    wavout = os.path.join(outdir) + "/{name}".format(name=filename)
    cerevoice_eng.CPRCEN_engine_speak_to_file(engine, input_str, wavout)
    #sys.stderr.write("INFO: wrote wav file '%s'\n" % wavout)

    # Clean up
    cerevoice_eng.CPRCEN_engine_delete(engine)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("string")
    parser.add_argument("filename")
    parser.add_argument("directory")

    args = parser.parse_args()

    synth(args.string, args.filename, args.directory)
