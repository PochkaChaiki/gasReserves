import openpyxl as xl
# from openpyxl.styles import *
import openpyxl.worksheet.worksheet as wsxl
import pandas as pd
from PIL import Image as PILImage
from openpyxl.drawing.image import Image
import io
import os

def copy_sheet(source_wb: xl.Workbook, source_sheet_name: wsxl.Worksheet, target_wb: xl.Workbook, target_sheet_name: wsxl.Worksheet):
    source_sheet = source_wb[source_sheet_name]
    target_sheet = target_wb.create_sheet(title=target_sheet_name)

    for row in source_sheet.iter_rows(values_only=False):
        for cell in row:
            new_cell = target_sheet.cell(row=cell.row, column=cell.column, value=cell.value)
            if cell.has_style:
                new_cell.font = xl.styles.Font(**cell.font.__dict__)
                new_cell.border = xl.styles.Border(**cell.border.__dict__)
                new_cell.fill = xl.styles.PatternFill(**cell.fill.__dict__)
                # new_cell.number_format = xl.styles.NumberFormat(**cell.number_format.__dict__)
                new_cell.protection = xl.styles.Protection(**cell.protection.__dict__)
                new_cell.alignment = xl.styles.Alignment(**cell.alignment.__dict__)

    for merged_cell in source_sheet.merged_cells:
        target_sheet.merge_cells(range_string=merged_cell.coord)



# ---------------------------------------------------------------------------------------------
# Data dict: 
# data = {
#     "placement1": {
#         "stat_params": {
#             "var": {
#                 "distribution": str,
#                 "params": str,
#             },    
#         },
#         "init_data": dict,
#         "prod_profile_init_data": dict,
#         "profiles_report": pd.DataFrame,
#         "images": {"hist": bytes, "tornado": bytes, "profile": bytes}
#     }, 
#     "placement2": {
#         ...
#     },
#     "placement3": {
#         ...
#     },
#     ...
# }
# ---------------------------------------------------------------------------------------------

def insert_to_sheet(data: dict, sheet: wsxl.Worksheet):
    vars = ['area', 'effective_thickness', 'porosity_coef', 'gas_saturation_coef']
    stat_params: dict = data['stat_params']
    for index in range(0, 4, 1):
        sheet[f'F{index+11}'] = stat_params[vars[index]]['distribution']
        sheet[f'H{index+11}'] = stat_params[vars[index]]['params']
    
    sheet['E102'].value = stat_params['permeability']['distribution']
    sheet['G102'].value = stat_params['permeability']['params']

    init_data: dict = data['init_data']
    sheet['K15'].value = init_data['relative_density']
    sheet['K16'].value = init_data['reservoir_temp']
    sheet['K17'].value = init_data['init_reservoir_pressure']
    sheet['K18'].value = init_data['temp_correction']
    sheet['K19'].value = init_data['init_overcompress_coef']
    sheet['F21'].value = init_data['num_of_vars']

    prod_profile_init_data: dict = data['prod_profile_init_data']
    sheet['J105'].value = prod_profile_init_data['prod_rate']
    sheet['J106'].value = prod_profile_init_data['operations_ratio']
    sheet['J107'].value = prod_profile_init_data['reserve_ratio']
    sheet['J108'].value = prod_profile_init_data['machines_num']
    sheet['J109'].value = prod_profile_init_data['time_to_build']
    sheet['J111'].value = prod_profile_init_data['well_height']
    sheet['J112'].value = prod_profile_init_data['pipe_diameter']
    sheet['J113'].value = prod_profile_init_data['main_gas_pipeline_pressure']
    sheet['J115'].value = prod_profile_init_data['abandon_pressure']
    sheet['J118'].value = prod_profile_init_data['filtr_resistance_A']
    sheet['J119'].value = prod_profile_init_data['filtr_resistance_B']
    sheet['J120'].value = prod_profile_init_data['macro_roughness_l']
    sheet['J121'].value = prod_profile_init_data['trail_length']
    sheet['J122'].value = prod_profile_init_data['input_cs_temp']
    
    profiles_report: pd.DataFrame = data['profiles_report']
    sheet['C25'].value = profiles_report['P90']['geo_gas_reserves']
    sheet['C27'].value = profiles_report['P50']['geo_gas_reserves']
    sheet['C29'].value = profiles_report['P10']['geo_gas_reserves']
    for profile, col in zip(('P90', 'P50', 'P10'), ('F', 'H', 'J')):
        vars = profiles_report[profile]
        sheet[f'{col}141'].value = vars['geo_gas_reserves']
        sheet[f'{col}142'].value = vars['effective_thickness']
        sheet[f'{col}143'].value = vars['porosity_coef']
        sheet[f'{col}144'].value = vars['gas_saturation_coef']
        sheet[f'{col}145'].value = vars['relative_density']
        sheet[f'{col}146'].value = vars['reservoir_temp']
        sheet[f'{col}147'].value = vars['init_reservoir_pressure']
        sheet[f'{col}148'].value = vars['temp_correction']
        sheet[f'{col}149'].value = vars['init_overcompress_coef']
        sheet[f'{col}150'].value = vars['annual_production']
        sheet[f'{col}151'].value = vars['accumulated_production']
        sheet[f'{col}152'].value = vars['kig']
        sheet[f'{col}153'].value = vars['num_of_wells']
        sheet[f'{col}154'].value = vars['years']
    
    images = data['images']
    for img_name, img_data in images.items():
        # Открываем изображение с помощью Pillow
        img = PILImage.open(io.BytesIO(img_data))

        # Сохраняем изображение во временный файл
        temp_img_path = f"temp_{img_name}.png"
        img.save(temp_img_path)

        # Вставляем изображение в Excel
        img_excel = Image(temp_img_path)
        if img_name == "hist":
            sheet.add_image(img_excel, 'B48')
        elif img_name == "tornado":
            sheet.add_image(img_excel, 'B74')
        elif img_name == "profile":
            sheet.add_image(img_excel, 'B124')
        # os.remove(temp_img_path)


def create_report(data: dict, template_path: str, output_path: str):
    # template_path = 'Шаблон отчета.xlsx'
    # output_path = 'Отчёт.xlsx'

    prod_sites = data.keys()

    template_wb = xl.load_workbook(template_path)
    output_wb = xl.Workbook()

    # Удаляем лист по умолчанию, который создается при создании нового рабочего файла
    if 'Sheet' in output_wb.sheetnames:
        del output_wb['Sheet']

    for placement in prod_sites:
        copy_sheet(template_wb, 'Sheet1', output_wb, placement)
        insert_to_sheet(data[placement], output_wb[placement])


    # ws = output_wb.active

    # for cellObj, val in zip(ws['M1':'M5'], [1, 2, 3, 4, 5]):
    #     for cell in cellObj:
    #         cell.value = val
    # print(ws['M1':'M5'])

    output_wb.save(output_path)

    

    print(f'Файл {output_path} успешно создан.')


# create_report({'Месторождение1': {}}, 'Шаблон отчета.xlsx', 'Отчёт.xlsx')