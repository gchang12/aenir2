from aenir2.quintessence import Morph
from aenir2.name_lists import character_list

def test_lara(path=0):
    game='5'
    unit='Lara'
    args=game,unit
    x=Morph(*args)
    names='levels','classes','stats'
    for i in range(3):
        if i == 0:
            x.promote(path)
        else:
            x.promote()
        attributes=x.my_levels,x.my_classes,x.my_stats
        for name,att in zip(names,attributes):
            print(att)
        print()


def test_trainee(unit='Ross',paths=(2,1,1)):
    trainees='Ross','Amelia','Ewan'
    assert unit in trainees
    kwargs={}
    game='8'
    kwargs['game']=game
    kwargs['unit']=unit
    x=Morph(**kwargs)
    def max_out(path):
        x.level_up(20)
        x.promote(path)
    attribute_names='levels','classes','stats','maxes','promo'
    for path in paths:
        attributes=x.my_levels,x.my_classes,x.my_stats,x.my_maxes,x.my_promotions
        for attribute,name in zip(attributes,attribute_names):
            print(name,attribute)
        print()
        max_out(path)
    x.promote()
    print(x.my_levels)
    url='https://serenesforest.net/the-sacred-stones/characters/average-stats/'
    url+=unit.lower()+'/'
    print(url)
    x.promote()


def test_hugh(num_times=3):
    args='6','Hugh'
    x=Morph(*args)
    print(x.my_stats)
    print(x.my_levels)
    x.decline_hugh(num_times)
    print(x.my_stats)
    x.level_up(5)
    x.promote()
    print(x.my_stats)
    hugh_avg='https://serenesforest.net/binding-blade/characters/average-stats/normal-mode/hugh-5000g/'
    print(hugh_avg)


def test_stat_booster(stat_name='HP'):
    args='6','Thany'
    x=Morph(*args)
    print(x.my_stats)
    x.use_stat_booster(stat_name)
    print(x.my_stats)


def test_hard_mode(chapter='16'):
    assert chapter in ('12','16','20','22')
    args='6','Cath'
    x=Morph(*args)
    print(x.my_stats,x.my_levels)
    x.add_hm_bonus(chapter=chapter)
    print(x.my_stats,x.my_levels)


def test_auto_level(chapter='13'):
    assert chapter in ('9','13')
    args='8','Amelia'
    x=Morph(*args)
    print(x.base_stats,x.my_levels.copy())
    x.add_auto_bonus(chapter)
    print(x.my_stats,x.my_levels)
    print(x.my_stats-x.base_stats)


def test_fe8_lord():
    def print_stats(game,unit):
        args=game,unit
        x=Morph(*args)
        base_lv=x.my_levels[0]
        print(*args)
        print(x.my_stats,x.my_levels.copy())
        x.add_auto_bonus()
        print(x.my_stats,x.my_levels)
        bonus=x.my_stats-x.base_stats
        bonus/=(15-base_lv)
        print(bonus)
        print(x.growth_rates/100)
    game='8'
    eirika='Eirika'
    ephraim='Ephraim'
    print_stats(game,eirika)
    print_stats(game,ephraim)


def test_fe7_lord(max_out=False,unit='Eliwood'):
    fe7_lords='Eliwood','Hector','Lyn'
    assert unit in fe7_lords
    args='7',unit
    x=Morph(*args)
    print(x.my_levels)
    print(x.my_stats)
    if max_out:
        x.level_up(19)
    x.promote()
    print(x.my_levels,x.my_stats)
    url='https://serenesforest.net/blazing-sword/characters/average-stats/eliwood/'
    print(url)


def test_fe7_dancer(unit='Ninian',in_list=False):
    assert unit in ('Ninian','Nils')
    if in_list:
        fe7_unit_list=character_list('7')
        y=unit in fe7_unit_list
        for person in fe7_unit_list:
            print(person)
        print('\nNils in unit list: %s'%y)
        return
    args='7',unit
    x=Morph(*args)
    print(x.base_stats)
    x.level_up(20)
    print(x.my_stats)
    print(x.maximum_stats)
    url='https://serenesforest.net/blazing-sword/characters/average-stats/nils/'
    print(url)

def test_gonzales(test_auto=False,chapter='10B'):
    game='6'
    unit='Gonzales'
    args=game,unit
    x=Morph(*args)
    print(args)
    if test_auto:
        print(x.my_stats,x.my_levels)
        x.add_auto_bonus(chapter)
        print(x.my_stats,x.my_levels)
        print(x.my_stats == x.base_stats)
        return
    print('Hard Mode: True\n')
    x.add_hm_bonus()
    l=x.my_stats,x.my_classes,x.my_levels,x.my_maxes
    for L in l:
        print(L)
    print()
    x.level_up(15)
    x.promote()
    m=x.my_stats,x.my_classes,x.my_levels,x.my_maxes
    for M in m:
        print(M)
    print()
    url='https://serenesforest.net/binding-blade/characters/average-stats/gonzales-dir/'
    print(url)


def test_wallace(lyn_mode):
    game='7'
    unit='Wallace'
    x=Morph(game,unit,lyn_mode=lyn_mode)
    print(x.unit_info)
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)
    x.level_up(8)
    x.promote()
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)


def test_fe4_lord():
    game='4'
    unit='Celice'
    args=game,unit
    x=Morph(*args)
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)
    x.promote()
    x.level_up(10)
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)


def test_fe4_jagen():
    game='4'
    unit='Sigurd'
    args=game,unit
    x=Morph(*args)
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)
    x.promote()
    x.level_up(10)
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)


def test_fe4_kid(male):
    game='4'
    unit=('Skasaher' if male else 'Lakche')
    father='Lex'
    kwargs={
        'game':game,\
        'unit':unit,\
        'father':father
        }
    x=Morph(**kwargs)
    print(kwargs)
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)
    x.promote()
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)


def test_unit(game,unit,lyn_mode=False,father='Arden'):
    x=Morph(game,unit,lyn_mode=lyn_mode,father=father)
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)
    x.level_up(20)
    x.promote()
    x.level_up(20)
    print(x.my_stats,x.my_levels,x.my_classes,x.my_maxes)

if __name__ == '__main__':
    #test_trainee()
    #test_lara()
    test_fe7_lord()
    #test_hugh()
    #test_wallace(False)
    #test_fe4_jagen()
    #test_fe7_dancer()
    #test_fe4_kid(True)
    #test_unit('6','Dayan')
    #test_gonzales()
