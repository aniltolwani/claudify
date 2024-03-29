import os
import click

def get_file_content(file_path):
    """
    Retrieves the content of files
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except UnicodeDecodeError:
            return f"Error decoding file: {file_path}"

def build_directory_tree(path, indent=0, file_paths=[]):
    """
    Builds a string representation of the directory tree and collects file paths.
    """
    tree_str = ""
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            tree_str += '    ' * indent + f"[{item}/]\n"
            tree_str += build_directory_tree(item_path, indent + 1, file_paths)[0]
        else:
            tree_str += '    ' * indent + f"{item}\n"
            # Indicate which file extensions should be included in the prompt!
            if item.endswith(('.py', '.md')):
                file_paths.append((indent, item_path))
    return tree_str, file_paths

def retrieve_directory_info(path):
    """
    Retrieves and formats directory information, including README (if present), the directory tree,
    and file contents.
    """
    readme_path = os.path.join(path, 'README.md')
    if os.path.exists(readme_path):
        readme_content = get_file_content(readme_path)
        formatted_string = f"README.md:\n```\n{readme_content}\n```\n\n"
    else:
        formatted_string = "README.md: Not found\n\n"

    directory_tree, file_paths = build_directory_tree(path)

    formatted_string += f"Directory Structure:\n{directory_tree}\n"

    for indent, file_path in file_paths:
        file_content = get_file_content(file_path)
        formatted_string += '\n' + '    ' * indent + f"{os.path.relpath(file_path, path)}:\n" + '    ' * indent + '```\n' + file_content + '\n' + '    ' * indent + '```\n'

    return formatted_string

@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-o', '--output', type=click.Path(dir_okay=False), default='formatted_directory_info.txt', help='Output file name (default: formatted_directory_info.txt)')
def main(directory, output):
    """
    Retrieve directory information and save it to a file.
    """
    formatted_directory_info = retrieve_directory_info(directory)
    with open(output, 'w', encoding='utf-8') as file:
        file.write(formatted_directory_info)

    click.echo(f"Directory information has been saved to {output}")

if __name__ == '__main__':
    main()