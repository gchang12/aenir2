from os.path import sep, exists
import os    
from aenir2 import save_stats
from aenir2.gender_dict import gender_dict
import pandas as pd


def collect_table(table,headers,rows,files):
    with open(table,'r') as r_file:
        for line in r_file.readlines():
            line=line.strip().split(',')
            for stat in line:
                file=table.split(sep)[-1]
                if file not in headers:
                    headers+=[file]
                if stat not in rows.keys():
                    rows[stat]=['' for n in range(len(files))]
                column_num=files.index(file)
                stat_loc=line.index(stat)
                rows[stat][column_num]=str(stat_loc)
            break


def rows_and_headers_for(game):
    rows={}
    raw_data_path=('.','raw_data','fe'+game)
    raw_data_path=sep.join(raw_data_path)
    headers=[]
    for root,folders,files in os.walk(raw_data_path):
        if not folders:
            continue
        for file in files:
            table=(raw_data_path,file)
            table=sep.join(table)
            collect_table(table,headers,rows,files)
    return rows,headers


def save_header_info(game):
    rows,headers=rows_and_headers_for(game)
    filename='table_headers.csv'
    path='.','raw_data','fe'+game,'metadata',filename
    metadata_dir=sep.join(path[:-1])
    if not exists(metadata_dir):
        os.mkdir(metadata_dir)
    path=sep.join(path)
    with open(path,'w') as w_file:
        header_row=','+','.join(headers)
        w_file.write(header_row)
        for key,cells in rows.items():
            w_file.write('\n'+key+',')
            for cell in cells:
                y=(cell+',' if cell else ',')
                w_file.write(y)


def index_for_name(table,in_filename,stat_name):
    d={}
    headers={}
    start=0
    stop=0
    with open(table,'r') as r_file:
        for line in r_file.readlines():
            line=line.strip().split(',')
            stat=line[0]
            if not stat:
                for col_num,name in enumerate(line):
                    if name.find(in_filename) >= 0:
                        headers[col_num]=name
            else:
                if stat == stat_name:
                    for col_num,cell in enumerate(line):
                        if col_num not in headers.keys():
                            continue
                        if cell.isdigit():
                            d[headers[col_num]]=int(cell)
    return d


def name_for_index(table,index,find_in):
    headers={}
    names={}
    with open(table,'r') as Rfile:
        for line in Rfile.readlines():
            line=line.strip().split(',')
            stat=line[0]
            if not stat:
                for col_num,name in enumerate(line):
                    if name.find(find_in) != -1:
                        headers[col_num]=name
            else:
                for col_num,cell in enumerate(line):
                    if not cell.isdigit():
                        continue
                    if col_num not in headers.keys():
                        continue
                    if int(cell) == index:
                        names[headers[col_num]]=stat
    return names


def search_tables(game,x,in_filename):
    header_path='.','raw_data','fe'+game
    header_path=sep.join(header_path)
    if not exists(header_path):
        for k in range(4,10):
            save_header_info(str(k))
    search_results={}
    if type(x) == str:
        kwargs={'in_filename':in_filename,'stat_name':x}
        s=lambda table: index_for_name(table,**kwargs)
    elif type(x) == int:
        s=lambda table: name_for_index(table,x,in_filename)
    else:
        return {}
    for root,folders,files in os.walk(header_path):
        for file in files:
            table=(root,file)
            table=sep.join(table)
            search_results[file]=s(table)
    print(game)
    for result in search_results.values():
        for key,val in result.items():
            print(key,val)


def search_all_tables(x,in_filename):
    for k in range(4,10):
        game=str(k)
        args=(game,x,in_filename)
        search_tables(*args)
        print('\n')


def is_father(unit):
    file=('.','raw_data','fe4','characters_base-stats1.csv')
    file=sep.join(file)
    gen1_bases=pd.read_csv(file)
    parent_list=gen1_bases['Name'].values
    return unit in parent_list


def column_extractor(game,in_filename,index):
    assert type(index) in (str,int)
    data_folder=('.','raw_data','fe'+game)
    data_folder=sep.join(data_folder)
    names=()
    for root,folders,files in os.walk(data_folder):
        for file in files:
            if file.find(in_filename) < 0:
                continue
            data_file=(data_folder,file)
            data_file=sep.join(data_file)
            data=pd.read_csv(data_file)
            if type(index) == int:
                column=data.iloc[:,index]
            else:
                if index in data.columns:
                    column=data.loc[:,index]
            for val in column.values:
                #   Ignore numbers in FE4 bases-3
                if val.isdigit():
                    continue
                #   For HM blokes whose rowspan exceeds 1
                if 'HM' in val:
                    continue
                #   For FE4 kids
                if is_father(val) and column.name == 'Character':
                    continue
                #   For FE7 Wallace
                wallace_exception=(
                    val == 'General',\
                    column.name == 'Name',\
                    in_filename.find('classes') < 0
                    )
                if all(wallace_exception):
                    continue
                names+=(val,)
    return names


def character_bases(game):
    kwargs={
        'game':game,
        'in_filename':'base-stats',
        'index':'Class'}
    class_list=column_extractor(**kwargs)
    kwargs['index']=0
    character_list=column_extractor(**kwargs)
    char_to_class={}
    for cls,char in zip(class_list,character_list):
        #print(cls,char)
        char_to_class[char]=cls
    return char_to_class


def test_table_searcher():
    kwargs={}
    kwargs['x']=0
    kwargs['in_filename']='base-stats'
    results=search_all_tables(**kwargs)
    for game,dictionaries in results.items():
        print(game)
        for path,index in dictionaries.items():
            print(path,index)
    

def class_maxes(game):
    if game == '5':
        return ()
    kwargs={
        'game':game,
        'in_filename':'maximum-stats',
        'index':'Class'}
    class_list=column_extractor(**kwargs)
    return class_list


def class_promo(game):
    all_classes=()
    if game == '7':
        file=('.','metadata','fe7_promo.csv')
        file=sep.join(file)
        columns=pd.read_csv(file,header=None)
        unpromoted=columns.iloc[:,0].values
        promoted=columns.iloc[:,1].values
        all_classes+=tuple(unpromoted)+tuple(promoted)
        return all_classes
    kwargs={
        'game':game,
        'in_filename':'promotion-gains'}
    col_names='Class','Promotion'
    for name in col_names:
        kwargs['index']=name
        class_list=column_extractor(**kwargs)
        all_classes+=class_list
    return all_classes


def class_growths(game):
    if game not in ('6','7'):
        return ()
    index=('Name' if game == '7' else 'Class')
    kwargs={
        'game':game,
        'in_filename':'classes_growth-rates',
        'index':index}
    class_list=column_extractor(**kwargs)
    return class_list


from aenir2.gender_dict import gender_dict


def bases_class_in_list(game,compare_list):
    #   For comparing character bases list to class attribute lists
    list_to_audit=character_bases(game)
    match_list=compare_list(game)
    gender=gender_dict(game)
    unmatched_items=set()
    for char,cls in list_to_audit.items():
        suffix=gender[char]
        if cls in match_list:
            continue
        else:
            gendered_class=cls+suffix
            if gendered_class in match_list:
                continue
            else:
                unmatched_items|={cls,gendered_class}
    write_difference(game,character_bases,compare_list,unmatched_items)
    return unmatched_items


def read_class_names(game,audit_list,match_list):
    d={}
    if game == '5':
        return
    d[character_bases]='bases'
    d[class_growths]='growths'
    d[class_maxes]='maxes'
    d[class_promo]='promo'
    filename=r'fe'+game+'.csv'
    classes_table=('.','metadata','class_names',filename)
    classes_table=sep.join(classes_table)
    s=()
    audit_match=[d[audit_list],d[match_list]]
    with open(classes_table) as r_file:
        for line in r_file.readlines():
            line=line.strip()
            line=line.split(',')
            s+=(line,)
    start=None
    stop=None
    for num,name in enumerate(s):
        if name == audit_match:
            start=num
        if not name[0] and start is not None:
            stop=num
            break
    if None in (start,stop):
        return {}
    else:
        return dict(s[start:stop])


def compare_class_lists(game,audit_list,match_to_list):
    #   For comparing class growths, promotion, and maxes lists
    list_to_audit=audit_list(game)
    list_to_match=match_to_list(game)
    unmatched=set()
    for cls in list_to_audit:
        if cls not in list_to_match:
            unmatched|={cls}
    write_difference(game,audit_list,match_to_list,unmatched)
    return unmatched


def write_difference(game,audit_list,match_to_list,difference):
    if not match_to_list(game) or not audit_list(game):
        return
    d={}
    d[character_bases]='character-bases'
    d[class_growths]='class-growths'
    d[class_maxes]='class-maxes'
    d[class_promo]='class-promo'
    part1=d[audit_list]
    part2=d[match_to_list]
    filename=(part1,part2)
    filename='classes_in_'+'_not-in_'.join(filename)+'.txt'
    path=('.','raw_data','fe'+game,'metadata',filename)
    diff_dir=sep.join(path[:-1])
    if not exists(diff_dir):
        os.mkdir(diff_dir)
    path=sep.join(path)
    with open(path,'w') as wFile:
        for name in difference:
            wFile.write(name+'\n')


def section_in_base_class_list(game,compare_list):
    base_class_dict=character_bases(game)
    genders=gender_dict(game)
    list_to_audit=compare_list(game)
    gendered_class_list=set()
    for character,cls in base_class_dict.items():
        gender=genders[character]
        gendered_class_list|={cls+gender}
    unmatched=set()
    for cls in list_to_audit:
        if cls in gendered_class_list:
            continue
        elif cls in base_class_dict.values():
            continue
        else:
            unmatched|={cls}
    write_difference(game,compare_list,character_bases,unmatched)
    return unmatched


def compile_all():
    class_attributes=class_maxes,class_promo,class_growths
    kwargs={}
    for k in range(4,10):
        game=str(k)
        kwargs['game']=game
        save_header_info(game)
        f=lambda attr1,attr2: compare_class_lists(game,attr1,attr2)
        for attribute in class_attributes:
            kwargs['compare_list']=attribute
            bases_class_in_list(**kwargs)
            section_in_base_class_list(**kwargs)
        for attribute in class_attributes:
            if attribute is class_attributes[-1]:
                break
            attr_loc=class_attributes.index(attribute)
            for sub_attr in class_attributes[attr_loc+1:]:
                f(attribute,sub_attr)
                f(sub_attr,attribute)


if __name__ == '__main__':
    #search_all_tables(x=0,in_filename='classes')
    #search_tables(game='4',x=0,in_filename='_')
    #compile_all()
    for k in range(4,10):
        game=str(k)
        save_header_info(game)