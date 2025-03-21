# uncompyle6 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.7.16 (default, Jan 17 2023, 16:06:28) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: gui\bot_config_fns.py
import distutils.command.config as config
from gui.creator import checkbox_fn_creator, train_fn_creator, write_bot_config, entry_int_fn_creator, entry_txt_fn_creator

from tkinter import StringVar, OptionMenu, Frame, Label, Entry, N, W

import webbrowser


def integer_entry_validate_cmd_creator(app, attr_name, def_value=0):
    def validate_cmd(value, action_type):
        if action_type == '1':
            if not value.isdigit():
                return False
            if len(value) > 1 and value[0] == '0':
                return False
        setattr(app.bot_config, attr_name, int(value if value != '' else str(def_value)))
        write_bot_config(app.bot_config, app.device.save_file_prefix)
        return True

    return validate_cmd


# restart
restart_checkbox = checkbox_fn_creator('enableStop', 'Auto Restart Game')
restart_do_round = entry_int_fn_creator('stopDoRound', 'Execute at every', 'round')

# break
break_do_round = entry_int_fn_creator('breakDoRound', 'Execute at every', 'round')
terminate_checkbox = checkbox_fn_creator('terminate', 'Terminate when break')
break_checkbox = checkbox_fn_creator('enableBreak', 'Take break at every end of round')

# Mystery Merchant
mystery_merchant_checkbox = checkbox_fn_creator('enableMysteryMerchant', 'Use resource buy item in Mystery Merchant')


def time_drop_down(app, parent):
    value = '{} Minute'.format(int(app.bot_config.breakTime / 60))
    options = [
        '1 Minute',
        '2 Minute',
        '3 Minute',
        '4 Minute',
        '5 Minute',
        '10 Minute',
        '15 Minute',
        '20 Minute',
        '25 Minute',
        '30 Minute',
        '40 Minute',
        '50 Minute',
        '60 Minute'
    ]
    variable = StringVar()
    variable.set(value)

    def command(value):
        app.bot_config.breakTime = int(value.replace(' Minute', '')) * 60
        write_bot_config(app.bot_config, app.device.save_file_prefix)

    option = OptionMenu(parent, variable, *options, command=command)
    return option, variable


building_checkbox = checkbox_fn_creator('enableBuilding', 'Nâng cấp thành phố')
# In city
collecting_checkbox = checkbox_fn_creator('enableCollecting', 'Collecting resource, troops, and help alliance')

produce_material = checkbox_fn_creator('enableMaterialProduce', 'Produce material')
material_do_round = entry_int_fn_creator('materialDoRound', 'Execute at every', 'round')

open_free_chest_in_tavern = checkbox_fn_creator('enableTavern', 'Open free chest in tavern')

training = checkbox_fn_creator('enableTraining', 'Auto upgrade and train troops')

train_barracks = train_fn_creator(
    'Barracks:',
    'trainBarracksTrainingLevel',
    'trainBarracksUpgradeLevel')

train_archery_range = train_fn_creator(
    'Archery:',
    'trainArcheryRangeTrainingLevel',
    'trainArcheryRangeUpgradeLevel')

train_stable = train_fn_creator(
    'Stable:',
    'trainStableTrainingLevel',
    'trainStableUpgradeLevel')

train_siege = train_fn_creator(
    'Siege:',
    'trainSiegeWorkshopTrainingLevel',
    'trainSiegeWorkshopUpgradeLevel')

# other
daily_vip_point_and_chest = checkbox_fn_creator('enableVipClaimChest', 'Claim daily vip point and chest')
vip_do_round = entry_int_fn_creator('vipDoRound', 'Execute at every', 'round')

claim_quest_checkbox = checkbox_fn_creator('claimQuests', 'Claim quests and daily objectives')
quest_do_round = entry_int_fn_creator('questDoRound', 'Execute at every', 'round')

alliance_action_checkbox = checkbox_fn_creator('allianceAction', 'Thu thập tài nguyên đồng minh, quà tặng và quyên góp công nghệ')
alliance_do_round = entry_int_fn_creator('allianceDoRound', 'Thực hiện mỗi ngày', 'lượt')
mail_checkbox = checkbox_fn_creator('enableMail', 'Đọc thư')
mail_system_checkbox = checkbox_fn_creator('mailSystem', 'Thư hệ thống')
mail_report_checkbox = checkbox_fn_creator('mailReport', 'Thư báo cáo')
mail_alliance_checkbox = checkbox_fn_creator('mailAlliance', 'Thư liên minh')
chat_checkbox = checkbox_fn_creator('enableChat', 'Chat')
chat_entry = entry_int_fn_creator('chatEntry', 'Nội dung chat')

# Outside

attack_barbarians_checkbox = checkbox_fn_creator('attackBarbarians', 'Attack Barbarians')
hold_position_checkbox = checkbox_fn_creator('holdPosition', 'Hold Position After Attack')
heal_troops_checkbox = checkbox_fn_creator('healTroopsBeforeAttack', 'Heal Troops Before Attack')
use_daily_ap_checkbox = checkbox_fn_creator('useDailyAPRecovery', 'Use Daily AP Recovery')
use_normal_ap_checkbox = checkbox_fn_creator('useNormalAPRecovery', 'Use Normal AP Recovery')
barbarians_base_level_entry = entry_int_fn_creator('barbariansBaseLevel', 'Base Level(normal/kvk):')
barbarians_min_level_entry = entry_int_fn_creator('barbariansMinLevel', 'Minimum attack Level:')
barbarians_max_level_entry = entry_int_fn_creator('barbariansMaxLevel', 'Maximum attack Level:')
number_of_attack_entry = entry_int_fn_creator('numberOfAttack', 'Number of Attack:')
timeout_entry = entry_int_fn_creator('timeout', 'Timeout (Second):')
return_attack_checkbox = checkbox_fn_creator('returnAttack', 'Quay về thành phố sau khi tấn công')

# Gem
gather_gem_checkbox = checkbox_fn_creator('enableGatherGem', 'Thu thập Gem')
gem_no_secondery_commander = checkbox_fn_creator('gatherGemNoSecondaryCommander', 'Không sử dụng chỉ huy phụ')
gem_start_with_coordinate = checkbox_fn_creator('gatherGemStartWithCord', 'Đi đến tọa độ khi bắt đầu')
coordinates_gatherx_entry = entry_int_fn_creator('coordinatesGatherXEntry', 'Tọa độ X')
coordinates_gathery_entry = entry_int_fn_creator('coordinatesGatherYEntry', 'Tọa độ Y')
coordinates_gather_xwidth = entry_int_fn_creator('coordinateGatherXWidth', 'Khoảng cách trục X')
coordinates_gather_ywidth = entry_int_fn_creator('coordinateGatherYWidth', 'Khoảng cách trục Y')
#choose_window_gather_gem_checkbox = checkbox_fn_creator('chooseWindowGatherGem', 'Chọn cửa sổ')
gem_window1_name = entry_txt_fn_creator("Gem1", "Tên cửa sổ farm gem ")
# press_gem1_checkbox = checkbox_fn_creator('Gem1', 'Gem1')
# press_gem2_checkbox = checkbox_fn_creator('Gem2', 'Gem2')
# press_gem3_checkbox = checkbox_fn_creator('Gem3', 'Gem3')
# press_gem4_checkbox = checkbox_fn_creator('Gem4', 'Gem4')
# press_gem5_checkbox = checkbox_fn_creator('Gem5', 'Gem5')
# press_gem6_checkbox = checkbox_fn_creator('Gem6', 'Gem6')
# press_gem7_checkbox = checkbox_fn_creator('Gem7', 'Gem7')
# press_gem8_checkbox = checkbox_fn_creator('Gem8', 'Gem8')
# press_gem9_checkbox = checkbox_fn_creator('Gem9', 'Gem9')
# press_gem10_checkbox = checkbox_fn_creator('Gem10', 'Gem10')
# press_gem11_checkbox = checkbox_fn_creator('Gem11', 'Gem11')
# press_gem12_checkbox = checkbox_fn_creator('Gem12', 'Gem12')
# press_gem13_checkbox = checkbox_fn_creator('Gem13', 'Gem13')
# press_gem14_checkbox = checkbox_fn_creator('Gem14', 'Gem14')
# press_gem15_checkbox = checkbox_fn_creator('Gem15', 'Gem15')
# press_gem16_checkbox = checkbox_fn_creator('Gem16', 'Gem16')
#around_troops_checkbox = checkbox_fn_creator('aroundTroops', 'Thu thập xung quanh chỉ huy')
#around_coor_checkbox = checkbox_fn_creator('aroundCoor', 'Thu thập xung quanh tọa độ')
gather_resource_checkbox = checkbox_fn_creator('gatherResource', 'Thu thập tài nguyên')
resource_no_secondery_commander = checkbox_fn_creator('gatherResourceNoSecondaryCommander', 'Không dùng chỉ huy phụ')
use_gathering_boosts = checkbox_fn_creator('useGatheringBoosts', 'Dùng Buff tăng tốc thu thập')
hold_one_query_space_checkbox = checkbox_fn_creator('holdOneQuerySpace', 'Để lại 1 chỗ tấn công người man rợ')
enable_scout_checkbox = checkbox_fn_creator('enableScout', 'Mở sương mù')
enable_Investigation_checkbox = checkbox_fn_creator('enableInvestigation', 'Do thám hang, làng')
scout_do_round_entry = entry_int_fn_creator('scoutDoRound', 'Thực hiện', 'lượt')
delay_scout_entry = entry_int_fn_creator('delayScout', 'Thời gian delay', 'giây')
scout_village_cave_checkbox = checkbox_fn_creator('enableScoutVillageCave', 'Do thám hang theo tọa độ')
scout_map_type_entry = entry_txt_fn_creator('scoutMaptype', "Map type (A,B,C,D) ")

# Variable for rss transfer
rss_transfer_checkbox = checkbox_fn_creator('enableRssTx', 'Chuyển RSS')
coordinates_x_trans_entry = entry_int_fn_creator('coordinatesTransXEntry', 'Tọa độ X')
coordinates_y_trans_entry = entry_int_fn_creator('coordinatesTransYEntry', 'Tọa độ Y')

# Variable for debug
debug_checkbox = checkbox_fn_creator('enableDebug', 'Debug mode')
debug_param1_entry = entry_txt_fn_creator('debugParam1', "Param 1")
debug_param2_entry = entry_txt_fn_creator('debugParam2', "Param 2")

def resource_ratio(app, parent):
    label_texts = ['Food:', 'Wood:', 'Stone:', 'Gold:']
    attr_names = ['gatherResourceRatioFood',
                  'gatherResourceRatioWood',
                  'gatherResourceRatioStone',
                  'gatherResourceRatioGold']

    frame = Frame(parent)
    label_1 = Label(frame, text='Type:')
    label_2 = Label(frame, text='Ratio:')
    label_1.grid(row=0, column=0, sticky=N + W, padx=(0, 5))
    label_2.grid(row=1, column=0, sticky=N + W, padx=(0, 5))
    for col in range(4):
        str_value = StringVar()
        str_value.set(str(getattr(app.bot_config, attr_names[col])))

        label = Label(frame, text=label_texts[col])
        entry = Entry(frame, textvariable=str_value)

        def creator(attr_name):
            def validate_cmd(value, action_type):
                if action_type == '1':
                    if not value.isdigit():
                        return False
                    if len(value) > 1 and value[0] == '0':
                        return False
                setattr(app.bot_config, attr_name, int(value if value != '' else '0'))
                write_bot_config(app.bot_config, app.device.save_file_prefix)
                return True

            return validate_cmd

        entry.config(validate='key', validatecommand=(
            frame.register(creator(attr_names[col])), '%P', '%d'
        ))
        label.grid(row=0, column=col + 1, sticky=N + W, padx=5)
        entry.grid(row=1, column=col + 1, sticky=N + W, padx=5)

        entry.config(width=10)
    return frame, None

bot_config_title_fns = [
    # [restart_checkbox, [restart_do_round]],
    [break_checkbox, [break_do_round]],
    # [scout_village_cave_checkbox, [scout_map_type_entry]],
    # [enable_scout_checkbox, [
    #     enable_Investigation_checkbox, 
    #     scout_do_round_entry, 
    #     delay_scout_entry
    # ]],
    # [gather_gem_checkbox,[
    #     gem_no_secondery_commander,
    #     gem_start_with_coordinate, 
    #     coordinates_gatherx_entry, 
    #     coordinates_gathery_entry, 
    #     coordinates_gather_xwidth,
    #     coordinates_gather_ywidth,
    #     gem_window1_name,
    # ]],
    [debug_checkbox, [debug_param1_entry, debug_param2_entry]],
    [rss_transfer_checkbox, [
        coordinates_x_trans_entry,
        coordinates_y_trans_entry
    ]]
]



"""
bot_config_title_fns = [
 [restart_checkbox, 
    [restart_do_round]],
 [break_checkbox, 
    [break_do_round, terminate_checkbox, time_drop_down]],
 [gather_gem_checkbox,
    [around_troops_checkbox, around_coor_checkbox, gem_no_secondery_commander, 
    coordinates_gatherx_entry, coordinates_gathery_entry, choose_window_gather_gem_checkbox, 
    press_gem1_checkbox, 
    press_gem2_checkbox, 
    press_gem3_checkbox, 
    press_gem4_checkbox, 
    press_gem5_checkbox, 
    press_gem6_checkbox, 
    press_gem7_checkbox, 
    press_gem8_checkbox, 
    press_gem9_checkbox, 
    press_gem10_checkbox, 
    press_gem11_checkbox, 
    press_gem12_checkbox, 
    press_gem13_checkbox, 
    press_gem14_checkbox, 
    press_gem15_checkbox, 
    press_gem16_checkbox]],
 [building_checkbox, []],
 [mystery_merchant_checkbox, []],
 [open_free_chest_in_tavern, []],
 [collecting_checkbox, []],
 [produce_material, 
    [material_do_round]],
 [daily_vip_point_and_chest, 
    [vip_do_round]],
 [claim_quest_checkbox, 
    [quest_do_round]],
 [alliance_action_checkbox, 
    [alliance_do_round]],
 [training, 
    [train_barracks, train_archery_range, train_stable, train_siege]],
 [mail_checkbox, 
    [mail_system_checkbox, mail_report_checkbox, mail_alliance_checkbox]],
 [attack_barbarians_checkbox,
    [hold_position_checkbox, 
    return_attack_checkbox, 
    heal_troops_checkbox, 
    use_daily_ap_checkbox, 
    use_normal_ap_checkbox, 
    barbarians_base_level_entry, 
    barbarians_min_level_entry, 
    barbarians_max_level_entry, 
    number_of_attack_entry, 
    timeout_entry]],
 [gather_resource_checkbox, 
    [use_gathering_boosts, hold_one_query_space_checkbox, resource_ratio, resource_no_secondery_commander]],
 [enable_scout_checkbox, 
    [enable_Investigation_checkbox, scout_do_round_entry, delay_scout_entry]],
 [scout_village_cave_checkbox, 
    [scout_do_round_entry]]]
"""
def callback(url):
    webbrowser.open_new(url)
