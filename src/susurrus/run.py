#!/usr/bin/env python

# %%

import argparse
import os
import sys
import whisper
import glob
import json
import openai


TITLE_PROMPT = """
Write a descriptive title for the following voice memo:
BEGIN VOICE MEMO:
{text}
END VOICE MEMO:
Descriptive Title:
"""

SUMMARY_PROMPT = """
Write a summary for the following voice memo:
BEGIN VOICE MEMO:
{text}
END VOICE MEMO:
Summary:
"""

ACTION_ITEM_PROMPT = """
Extract action items from the following voice memo:
BEGIN VOICE MEMO:
{text}
END VOICE MEMO:
Action Items:
"""

def process_title(result):
    """ Use the OpenAI API to generate a title for a voice memo """
    # Get the text of the voice memo
    text = result['text']
    # Generate a title
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=TITLE_PROMPT.format(text=text),
        temperature=0.5,
        max_tokens=256,
        stop=['\n']
    )
    # Add the title to the result
    result['title'] = response['choices'][0]['text']


def process_summary(result):
    """ Use the OpenAI API to generate a summary for a voice memo """
    # Get the text of the voice memo
    text = result['text']
    # Generate a summary
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=SUMMARY_PROMPT.format(text=text),
        temperature=0.5,
        max_tokens=256,
        stop=['\n']
    )
    # Add the summary to the result
    result['summary'] = response['choices'][0]['text']


def process_action_items(result):
    """ Use the OpenAI API to generate action items for a voice memo """
    # Get the text of the voice memo
    text = result['text']
    # Generate action items
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=ACTION_ITEM_PROMPT.format(text=text),
        temperature=0.5,
        max_tokens=256,
        stop=['\n']
    )
    # Add the action items to the result
    result['action_items'] = response['choices'][0]['text']


def main(model_name, audio_dir, output_dir, extra_processing=''):
    # Make sure the audio directory exists
    if not os.path.isdir(audio_dir):
        print('Audio directory does not exist')
        sys.exit(1)
    # Make sure the output directory exists, and create it if it doesn't
    os.makedirs(output_dir, exist_ok=True)

    print('Loading model', model_name)
    model = whisper.load_model(model_name)
    print('Model loaded')
    
    # Loop through all the .mp3 files in the audio directory
    for audio_file in glob.glob(os.path.join(audio_dir, '*.mp3')):
        # Get the output file path
        output_file = os.path.join(output_dir, os.path.basename(audio_file).replace('.mp3', '.json'))
        # Check if it exists, and load it if so
        if os.path.isfile(output_file):
            print('Loading existing output file', output_file)
            with open(output_file, 'r') as f:
                result = json.load(f)
        else:
            # Otherwise, transcribe the audio file
            print('Transcribing', audio_file)
            result = model.transcribe(audio_file)
            # Save the result to the output file
            with open(output_file, 'w') as f:
                json.dump(result, f)
        # Perform any extra processing
        for extra_step in extra_processing.split(','):
            print('Performing extra processing step', extra_step)
            if extra_step == 'title' and 'title' not in result:
                process_title(result)
            elif extra_step == 'summary' and 'summary' not in result:
                process_summary(result)
            elif extra_step == 'action_items' and 'action_items' not in result:
                process_action_items(result)
        # Save the result to the output file
        with open(output_file, 'w') as f:
            json.dump(result, f)

    print('Done!')


if __name__ == "__main__":
    # Parse command line arguments

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='base.en', help='Whisper model to use')
    parser.add_argument('--audio_dir', type=str, required=True, help='Directory containing audio files')
    parser.add_argument('--output_dir', type=str, required=True, help='Directory to write output files')
    parser.add_argument('--extra_processing', type=str, default='', help='Extra processing to perform on the output')
    args = parser.parse_args()

    main(args.model, args.audio_dir, args.output_dir, args.extra_processing)
