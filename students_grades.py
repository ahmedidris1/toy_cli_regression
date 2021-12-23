import csv
from math import sqrt

data_file = './data/sampleData.csv'


def load_csv(file_name):   
    ids = []
    names = []
    hours = []
    grades = []

    with open(file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            ids.append(int(row['id']))
            names.append(row['name'])
            hours.append(float(row['hours']))
            grades.append(float(row['score']))
            
    return {"ID":ids, "Name": names, 
            "Hours": hours, "Grade": grades}



def display_data(**kwargs):
    columns = kwargs.keys()
    values = kwargs.values()
    dataset = list(zip(*values))
    
    indent = f'{"":5}'
    
    def spacer(index, val):
        if index == 1:
            return f'{val:<20}'
        else:
            return f'{val:<10}'
        
    # columns_names = list( map(lambda index, x: spacer(index, x), enumerate(columns)) )
    columns_names = [spacer(index, val) for index, val in enumerate(columns)]
    table_header = indent + ''.join(columns_names)
    
    dashed_line_length = len(table_header)

    border_dashes = '-' * dashed_line_length 
    print(border_dashes)
    print(table_header)
    print(border_dashes)
    for i in range(len(dataset)):
        row_i_spaced = [spacer(index, val) for index , val in enumerate(dataset[i])]
        row_i = indent + ''.join(row_i_spaced)
        print(row_i)
    print(border_dashes)
    
dataset = load_csv(data_file)
display_data(**dataset)   
# display_data(ids, names, hours, scores)
    
    
def grade_to_alphapet(grade_numeric):
    if 90 <= grade_numeric <= 100:
        return 'A'
    elif grade_numeric >= 75:
        return 'B'
    elif grade_numeric >= 60:
        return 'C'
    elif grade_numeric >=50:
        return 'D'
    else: 
        return 'F'
    
    
def compute_grades(dataset):
    dataset_copy = dataset.copy()
    dataset_copy.pop('Hours', None)
    dataset_copy['Grade'] = list( map(grade_to_alphapet, dataset_copy['Grade']) )
    display_data(**dataset_copy)
    
# compute_grades(dataset)
# print(dataset)


def search_by_name(dataset):
    name = input('Please, enter the name you are looking for: ').lower()
    names_list = map(lambda x: x.lower() ,dataset['Name'])
    found_indices = [index for index, full_name in enumerate(names_list) if name in full_name]
    
    search_result_dict = {}
    
    for key in dataset:
        search_result_dict[key] = [dataset[key][i] for i in found_indices]
        
    display_data(**search_result_dict)
    
    
# search_by_name(dataset)


def mean(arr):
    return sum(arr) / len(arr)


def var(arr):
    arr_mean = mean(arr)
    diff = [(arr[i]-arr_mean)**2 for i in range(len(arr))]
    variance = sum(diff) / (len(diff) - 1)
    return round( variance, 2 )


def std(arr):
    return round(sqrt(var(arr)), 2)


def calculate_descriptive_statistics(dataset):
    
    hours = dataset['Hours']
    grades = dataset['Grade']
    
    print(var(hours))
    
    stats =  {
        '----': ['Hours', 'Score'],
        'Mean': [mean(hours), mean(grades)],
        'Variance': [var(hours), var(grades)],
        'Standard Deviation': [std(hours), std(grades)]
    }
    
    display_data(**stats)
    
# calculate_descriptive_statistics(dataset)


def calculate_regression_param(dataset, independent, dependent):
    x = dataset[independent]
    y = dataset[dependent]
    n = len(x)
    
    xy = [ x[i]*y[i] for i in range(n) ]
    x_square = [_x**2 for _x in x] 
    
    b1 = ( sum(xy) - n*mean(x)*mean(y) ) / ( sum(x_square) - n*mean(x)**2 )
    b0 = mean(y) - b1*mean(x)
    
    border = '-'*60
    regression_equation = f'Scores = {b0} + {round(b1, 3)} * Hours'
    
    # print(border)
    # print(regression_equation.center(60))
    # print(border)
    
    return b0, b1

    
# print( calculate_regression_param(dataset, 'Hours', 'Grade') )


def predict_grade(dataset, hours):
    b0, b1 = calculate_regression_param(dataset)
    
    return b0 + b1*hours


if '__name__' == '__main__':
    
    run = True

    operations = {
        "1": {"func": "read_data", "title": "Read Data"},
        "2": {"func": "list_data", "title": "List Data"},
        "3": {"func": 'compute_show_grades', "title": "Compute and Show Grades"},
        "4": {"func": 'search_by_name', "title": "Search by Name"},
        "5": {"func": 'descriptive_Stats', "title": "Descriptive Statistics"},
        "6": {"func": 'reg_analysis', "title": "Regression Analysis"},
        "7": {"func": 'predict_grade', "title": "Prediction"},
        "9": {"func": 'exit_system', "title": "Exit the System"}
    }
    
    dashed_line = '-'*60
    welcome_msg = f' Welcome to GRADES_STATS V1.0\nDesigned By Alaa Mirghani'
    
    operations_names = [operation["title"] for operation in operations.values()]
    
    print(operations_names)
    
    while run:
        pass