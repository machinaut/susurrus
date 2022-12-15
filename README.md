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

I used the Deep Learning Debian 10 base image, and installed [whisper](https://github.com/openai/whisper#setup) into a conda python 3.9 environment.

Copy the audio files to the remote machine:
```
gcloud compute instances start $SUSURRUS_INSTANCE && \
    sleep 30 && \
    rsync -ave ssh "$AUDIO_PATH/" $SUSURRUS_MACHINE:~/data/ && \
    gcloud compute ssh "$SUSURRUS_INSTANCE" --command "pip install --upgrade --no-deps --force-reinstall git+https://github.com/machinaut/susurrus.git && nohup python -m susurrus.run --model base --path ~/data --shutdown > ~/susurrus.log 2>&1 &"
```

## Thinking about the design

* Runs locally with small models
* Takes an input folder and output folders
* Language model processing of transcripts
  * Notes on the unreliability of these tools
  * Titling
  * Summarization
  * Extracting key points
  * Extracting todos/action items
  * Picking good tags for notes
  * Extracting good questions
  * Transforming into socratic dialogue
  * Examples on creating your own
* Processing ends up in a JSON file
  * Single file key-object list, keys are filenames, objects are all processed data
  * Example of gathering up all of the action items into a single list
* Include docs on launching google cloud instances
* Extra google cloud features
  * Upload audio files to storage bucket
  * Save transcripts to storage bucket
  * Auto-shutdown when processing is done
