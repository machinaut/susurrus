# susurrus

Helper package for using [Whisper](https://openai.com/blog/whisper) to process voice memos.
It includes a few language model processing steps, and a script to run the whole thing.

Also there is some documentation on how to start a google cloud instance with a GPU to run the `large` model.

## Installation

You probably want to use a virtual environment, with a version compatible with Whisper.

See [Whisper Docs](https://github.com/openai/whisper#setup).

```
# First install Whisper, see above.
git clone https://github.com/machinaut/susurrus
pip install -e susurrus
```

## Usage

```
python -m susurrus.run \
    --model base.en \
    --audio_dir /path/to/audio \
    --output_dir /path/to/output \
    --extra_processing title,summary,action_items
```

## Directory Layout

```
audio_dir/
    file_1.mp3
    file_2.mp3
    ...

output_dir/
    file_1.json
    file_2.json
    ...
```

## User Warnings

Generated action items might hallucinate things not in the transcript, or miss important things that are there.
It would be nice to do something like generate many action item lists and combine them to get a better result.

## Running on Google Cloud

The `large` Whisper model gives the best results, but needs a GPU.

For now I have been using a google cloud instance with a GPU, specifically a `n1-standard-8` with a `nvidia-tesla-p100` GPU.

I used the Deep Learning Debian 10 base image, and installed [whisper](https://github.com/openai/whisper#setup) into a conda python 3.9 environment.

I also created a storage bucket to store the audio files and the transcripts.  Upload files to the bucket:
```
gsutil -m rsync -r /my/audio/files/ gs://my-bucket/voice-memos/
```

I needed to create a storage account with read/write access and a [storage account JSON key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-gcloud), and then upload it to the instance in order to access the bucket.


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
