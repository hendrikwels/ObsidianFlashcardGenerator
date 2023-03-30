import os
import re
import openai


def generate_questions_for_files_with_hashtags(api_key, folder_path):
    # Authenticate with the OpenAI API using your API key
    openai.api_key = api_key
    prompt = "Füge eine Frage für den folgenden Text auf deutsch hinzu.\n"

    # Create a new directory to store the modified files
    new_folder_path = os.path.join(folder_path, 'AWS')
    os.makedirs(new_folder_path, exist_ok=True)

    # Get a list of all .md files in the specified folder that contain both the #aws and #cloud hashtags
    md_files = find_md_files_with_hashtags(folder_path)

    # Loop through each file and generate questions using the OpenAI API
    for file in md_files:
        print(f'Generating questions for {file}...')
        # Read the contents of the file
        with open(os.path.join(folder_path, file), 'r') as f:
            contents = f.read()

        paragraphs = contents.split('Break:')

        questions_per_paragraph = []
        for paragraph in paragraphs:

            print(paragraph)
            # Extract Images in the Paragraph
            image_pattern = re.compile(r'!\[\[Pasted image .*?\]\]')
            images = image_pattern.findall(paragraph)

            # Remove Images from the Paragraph
            paragraph = image_pattern.sub('', paragraph)

            questions = generate_questions(prompt + paragraph)
            questions_per_paragraph.append('\nSTART\nBasic\n')
            questions_per_paragraph.extend(questions.replace('?', '?\nBack:\n'))
            questions_per_paragraph.extend(paragraph)

            # Append the images after the Answer
            for image in images:
                questions_per_paragraph.append('\n' + image)

            questions_per_paragraph.append('\nTags: #aws #cloud #solutions_architect #tech_fundamentals')
            questions_per_paragraph.append('\nEND\n')

        new_contents = ''.join(questions_per_paragraph)

        # Write the modified contents to a new file in the new directory
        with open(os.path.join(new_folder_path, file), 'w') as f:
            f.write('TARGET DECK\nAWS SOLUTIONS ARCHITECT\n')
            f.write(new_contents)

    # Return the path to the new directory
    return new_folder_path


def find_md_files_with_hashtags(folder_path):
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    matching_files = []
    for file in md_files:
        with open(os.path.join(folder_path, file), 'r') as f:
            contents = f.read()
            if re.search(r'#aws', contents, re.IGNORECASE) and re.search(r'#cloud', contents, re.IGNORECASE):
                matching_files.append(file)
    return matching_files


def generate_questions(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": 'user', "content": f"{text}"}
        ]
    )
    reply_content = completion.choices[0].message.content
    return reply_content



api_key = open('api_key.txt', 'r').read().strip('\n')
folder_path = '/Users/hendrikwels/Library/Mobile Documents/iCloud~md~obsidian/Documents/Book Notes'
new_folder_path = generate_questions_for_files_with_hashtags(api_key, folder_path)
