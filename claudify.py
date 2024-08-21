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

def build_directory_tree(path, indent=0, file_paths=[], excluded_files=[], excluded_dirs=['node_modules']):
    """
    Builds a string representation of the directory tree and collects file paths.
    """
    tree_str = ""
    allowed_extensions = ('.tsx', '.ts', '.css', '.html', '.py', '.md','.js')
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            if item not in excluded_dirs:
                tree_str += '    ' * indent + f"[{item}/]\n"
                tree_str += build_directory_tree(item_path, indent + 1, file_paths, excluded_files, excluded_dirs)[0]
        else:
            if item not in excluded_files and item.endswith(allowed_extensions) and not item.endswith('.json'):
                tree_str += '    ' * indent + f"{item}\n"
                file_paths.append((indent, item_path))
    return tree_str, file_paths

def retrieve_directory_info(path, excluded_files=[], excluded_dirs=['node_modules']):
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

    directory_tree, file_paths = build_directory_tree(path, excluded_files=excluded_files, excluded_dirs=excluded_dirs)
    formatted_string += f"Directory Structure:\n{directory_tree}\n"

    for indent, file_path in file_paths:
        if not file_path.endswith('.json') and 'node_modules' not in file_path.split(os.path.sep):
            file_content = get_file_content(file_path)
            formatted_string += '\n' + '    ' * indent + f"{os.path.relpath(file_path, path)}:\n" + '    ' * indent + '```\n' + file_content + '\n' + '    ' * indent + '```\n'

    return formatted_string

@click.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('-o', '--output', type=click.Path(dir_okay=False), default='formatted_directory_info.txt', help='Output file name (default: formatted_directory_info.txt)')
@click.option('--exclude', multiple=True, help='File names to exclude (can be specified multiple times)')
@click.option('--exclude-dir', multiple=True, default=['node_modules'], help='Directory names to exclude (can be specified multiple times)')
def main(directory, output, exclude, exclude_dir):
    """
    Retrieve directory information and save it to a file.
    """
    formatted_directory_info = retrieve_directory_info(directory, excluded_files=list(exclude), excluded_dirs=list(exclude_dir))
    with open(output, 'w', encoding='utf-8') as file:
        file.write(formatted_directory_info)
    click.echo(f"Directory information has been saved to {output}")

if __name__ == '__main__':
    main()
