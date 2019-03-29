from bs4 import BeautifulSoup
from pathlib import Path
import argparse
import pandas as pd


def _kml_to_df(file_name):
    print('_kml_to_df: ' + file_name)
    kml_df = pd.DataFrame(columns=['Longitude', 'Latitude', 'Altitude', 'Name', 'Folder'])
    kml_df_index = 0

    with open(file_name, 'r') as f:
        contents = f.read()
        kml_soup = BeautifulSoup(contents, 'xml')
        folders = kml_soup.select('Folder')
        for folder in folders:
            folder_name = folder.find('name').getText()
            placemarks = folder.find_all('Placemark')
            for placemark in placemarks:
                point = placemark.find('Point')
                if point is not None:
                    name = placemark.find('name').getText()
                    coordinates = point.find('coordinates').getText().split(',')
                    kml_df.loc[kml_df_index, 'Folder'] = folder_name
                    kml_df.loc[kml_df_index, 'Name'] = name
                    kml_df.loc[kml_df_index, 'Longitude':'Altitude'] = coordinates
                    kml_df_index += 1
        return kml_df

        # Placemark
        placemarks = kml_soup.select('Folder Placemark')
        for index, placemark in enumerate(placemarks):
            pm_name = placemark.find('name').getText().replace(',', ';')
            pm_coordinates = placemark.find('coordinates').getText()
            pm_item = pm_coordinates + ',' + pm_name
            pm_item_list = pm_item.split(',')
            kml_df.loc[index] = pm_item_list
    return kml_df


def _write_excel_from_df(df, file_name):
    print('_write_excel_from_df: ' + file_name)
    df.to_excel(file_name, sheet_name='Hoja1')


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
            klm_df = _kml_to_df(file)
            _write_excel_from_df(klm_df, file.replace('.kml', '.xls'))


if __name__ == '__main__':
    main()
