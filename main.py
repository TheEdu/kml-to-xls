from bs4 import BeautifulSoup
from pathlib import Path
import argparse


def _kml_to_list(file):
    print('_kml_to_list: ' + file)
    kml = []
    with open(file, 'r') as f:
        contents = f.read()
        kml_soup = BeautifulSoup(contents, 'xml')

        # Placemark
        placemarks = kml_soup.select('Folder Placemark')
        for placemark in placemarks:
            pm_name = placemark.find('name').getText().replace(',', '')
            pm_coordinates = placemark.find('coordinates').getText()
            pm_item = pm_name + ',' + pm_coordinates + '\n'
            kml.append(pm_item)
    return kml


def _write_csv(name, rows):
    print('_write_csv: ' + name)
    csv_header = '\ufeff' + name.replace('.csv', '') + ',X,Y,Z' + '\n'
    with open(name, mode='w', encoding='utf-16le') as f:
        f.write(csv_header)
        for row in rows:
            f.write(row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l',
                        '--file-list',
                        nargs='+',
                        help='list of files to convert to csv',
                        default=['test.kml'])

    file_list = parser.parse_args().file_list

    for file in file_list:
        if (file.find('.kml') != -1 and Path(file).is_file()):
            kml = _kml_to_list(file)
            csv_name = file.replace('.kml', '.csv')
            _write_csv(csv_name, kml)


if __name__ == '__main__':
    main()
