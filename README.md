# susurrus

Helper package for using [Whisper](https://openai.com/blog/whisper) to process voice memos.
It includes a few language model processing steps, and a script to run the whole thing.

Also there is some documentation on how to start a google cloud instance with a GPU to run the `large` model.

## Installation

You probably want to use a virtual environment, with a version compatible with Whisper.

See [Whisper Docs](https://github.com/openai/whisper#setup) for installing instructions.

```
# First install Whisper
pip install --upgrade --no-deps --force-reinstall git+https://github.com/machinaut/susurrus.git
```

## Usage

```
python -m susurrus.run \
    --model base.en \
    --path /path/to/files \
    --extras title,summary,action_items
```

## User Warnings

Generated action items might hallucinate things not in the transcript, or miss important things that are there.
It would be nice to do something like generate many action item lists and combine them to get a better result.

## Running on Google Cloud

The `large` Whisper model gives the best results, but needs a GPU.

For now I have been using a google cloud instance with a GPU, specifically a `n1-standard-8` with a `nvidia-tesla-p100` GPU.

I used the Deep Learning Debian 10 base image, and installed [whisper](https://github.com/openai/whisper#setup) into a conda python 3.9 environment, and made sure that environment was activated when running susurrus.

Copy the audio files to the remote machine and update and run the susurrus package:
```
# Start machine
gcloud compute instances start $SUSURRUS_INSTANCE
# Sync audio to machine (however you want)
# To make this work: `gcloud compute config-ssh`
rsync -ave ssh "$AUDIO_PATH/" $SUSURRUS_MACHINE:~/data/
# On machine -- update susurrus package
pip install --upgrade --force-reinstall git+https://github.com/machinaut/susurrus.git
# On machine -- run susurrus
# If you have a conda environment, don't forget to activate it
susurrus --model large --path ~/data --openai-key $OPENAI_API_KEY --git-push --shutdown
# Rsync only the generated json files back to local machine
rsync -ave ssh "$SUSURRUS_MACHINE:~/data/*.json" "$VOICE_TRANSCRIPTS/"
```
