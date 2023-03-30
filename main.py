import os
import re
import openai


def generate_questions_for_obsidian_files(api_key, folder_path):
    """Main Function: Generates questions for all .md files in the specified folder
    that contain both the #aws and #cloud hashtags and returns the new Folder Path"""

    openai.api_key = api_key
    prompt = "Füge eine Frage für den folgenden Text auf deutsch hinzu.\n"

    new_folder_path = create_new_directory(folder_path)
    obsidian_files = find_obsidian_files_with_tags(folder_path)

    for file in obsidian_files:
        print(f'Generating questions for {file}...')
        contents = read_file_contents(os.path.join(folder_path, file))
        paragraphs = contents.split('Break:')

        question_per_paragraph = process_paragraphs(prompt, paragraphs)
        new_contents = ''.join(question_per_paragraph)

        write_modified_contents(new_folder_path, file, new_contents)

    return new_folder_path


def create_new_directory(folder_path):
    """Creates a new directory to store the modified files"""
    new_folder_path = os.path.join(folder_path, 'AWS')
    os.makedirs(new_folder_path, exist_ok=True)
    return new_folder_path


def read_file_contents(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def write_modified_contents(new_folder_path, file, new_contents):
    with open(os.path.join(new_folder_path, file), 'w') as f:
        f.write('TARGET DECK\nAWS SOLUTIONS ARCHITECT\n')
        f.write(new_contents)


def find_obsidian_files_with_tags(folder_path):
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    matching_files = []
    for file in md_files:
        contents = read_file_contents(os.path.join(folder_path, file))
        if re.search(r'#aws', contents, re.IGNORECASE) and re.search(r'#cloud', contents, re.IGNORECASE):
            matching_files.append(file)
    return matching_files[:1]


def process_paragraphs(prompt, paragraphs):
    question_per_paragraph = []
    for paragraph in paragraphs:
        question = generate_question(prompt + paragraph)
        question_per_paragraph.append('\nSTART\nBasic\n')
        question_per_paragraph.extend(question.replace('?', '?\nBack:\n'))
        question_per_paragraph.extend(paragraph)
        question_per_paragraph.append('\nTags: #aws #cloud #solutions_architect #tech_fundamentals')
        question_per_paragraph.append('\nEND\n')
    return question_per_paragraph


def generate_question(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": 'user', "content": f"{text}"}
        ]
    )
    reply_content = completion.choices[0].message.content
    return reply_content


api_key = read_file_contents('api.txt').strip('\n')
folder_path = '/Users/hendrikwels/Library/Mobile Documents/iCloud~md~obsidian/Documents/Book Notes'
new_folder_path = generate_questions_for_obsidian_files(api_key, folder_path)
