from lxml import objectify
import os
import glob


def fetch_labels_mapping():
    # If labels_mapping.txt is not found, we return an empty dictionary
    try:
        with open("labels_mapping.txt") as file:
            entry = [line.split("=") for line in file.readlines()]
        return {key.strip(): value.strip() for key, value in entry}
    except FileNotFoundError:
        print("Warning: labels_mapping.txt not found. No label mappings will be applied.")
        return {}


def fetch_allowed_labels():
    # Graceful handling if allowed_labels.txt is missing
    try:
        with open("allowed_labels.txt") as file:
            return [line.strip('\n') for line in file.readlines()]
    except FileNotFoundError:
        print("Warning: allowed_labels.txt not found. No label filtering will be applied.")
        return []


def _map_label(label, labels_mapping):
    if label in labels_mapping:
        return labels_mapping[label]
    else:
        return label


def _is_label_approved(label, approved_labels):
    return label in approved_labels


def convert_label(label, labels_mappings, approved_labels):
    mapped_label = _map_label(label, labels_mappings)

    if _is_label_approved(mapped_label, approved_labels):
        return mapped_label
    return None


def read_xml_file(file_path):
    with open(file_path) as file:
        return objectify.fromstring(file.read())


def read_xml_files(file_path):
    files = list()
    for file_name in file_path.split(';'):
        if os.path.isdir(file_name):
            xml_files = glob.glob(file_name + '/*.xml')
            for file in xml_files:
                files.append(read_xml_file(file))
        else:
            files.append(read_xml_file(file_name))

    return files
