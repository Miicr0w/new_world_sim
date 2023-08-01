import random 

def crit_dmg(crit_dmg,bonus_crit_dmg=0,con_150=False,amt_resil=5,int_50=False,prophet_of_a_fire_god=False):
    crit_dmg_prevented = 4.9*amt_resil
    if con_150:
        crit_dmg_prevented +=10
    if int_50:
        bonus_crit_dmg +=10
    if prophet_of_a_fire_god:
        bonus_crit_dmg +=15
    crit_dmg = 1+round(((crit_dmg+bonus_crit_dmg)-crit_dmg_prevented)/100,2) 

    if crit_dmg < 1:
        return 1
    
    return crit_dmg

def crit(base_crit,extra_crit=0,backstab_percent=0,keen=False,keen_awareness=False,spellslinger=False):
    if random.randint(1,100) <= backstab_percent:
        return True
    
    if keen:
        extra_crit += 12
    if keen_awareness:
        extra_crit += 12
    if spellslinger:
        extra_crit += 10

    crit_chance = round(2.1*base_crit+extra_crit,2)

    if random.randint(1,100) <= crit_chance:
        return True
    return False

def base_dmg(base_dmg,crit,crit_dmg,weight_class="medium",thwarting=False,attunement=False,shirking=False,shirking_percent=20,str_200=False,str_50=False,str_100=False,
             auto_percent=90,int_150=False,int_300=False,base_dmg_bonus=0,opal=True,opal_percentage=75,aversion=False,aversion_amt=5,
             pyromania=False,pyromania_chance=25,invig_punishment=True):
    
    weight_class_base_dmg = {
        "light": 20,
        "medium": 10,
        "heavy": 0
    }    

    base_dmg_bonus += weight_class_base_dmg[weight_class]
    if thwarting:
        base_dmg_bonus +=12
    if attunement:
        base_dmg_bonus +=12
    elif shirking:
        if random.randint(1,100) <= shirking_percent:
            base_dmg_bonus += 40
    if str_50:
        base_dmg_bonus +=10
    if str_100:
        base_dmg_bonus +=5
    if str_200:
        base_dmg_bonus +=10
    if int_300:
        base_dmg_bonus +=10
    if opal:
        if random.randint(1,100) <= opal_percentage:
            base_dmg_bonus+=15
    if pyromania:
        if random.randint(1,100) <= pyromania_chance:
            base_dmg_bonus+=10
    if invig_punishment:
        base_dmg_bonus += random.randint(0,32) // 4 # only even amounts
    if aversion:
        base_dmg_bonus -= 3.9*aversion_amt
    if crit: 
        base_dmg_bonus += (crit_dmg-1)*100

    dmg = int(base_dmg*(100+base_dmg_bonus)/100)
    return dmg

def empower_percentage(bonus_empower=0,keenly_empowered=False,shirking_empower=False,avg_shirking_empower_stacks=3,greed=False,
                       avg_greed_stacks=1.33,center_of_attention=False,center_of_attention_percentage=20,power_through_pain=False,
                       power_through_pain_percentage=75,hammer_time=False,hammer_time_percentage=25,clear_casting=False,clear_casting_percentage=80,
                       clear_mind=False,clear_mind_percentage=50,dmg_ring=False):
    if keenly_empowered:
        bonus_empower +=15
    if shirking_empower:
        bonus_empower +=3.9*avg_shirking_empower_stacks
    if greed:
        bonus_empower +=5*avg_greed_stacks
    if center_of_attention:
        if random.randint(1,100) <= center_of_attention_percentage:
            bonus_empower +=10
    if power_through_pain:
        if random.randint(1,100) <= power_through_pain_percentage:
            bonus_empower +=35
    if hammer_time:
        if random.randint(1,100) <= hammer_time_percentage:
            bonus_empower +=20
    if clear_casting:
        if random.randint(1,100) <= clear_casting_percentage:
            bonus_empower +=5
    if clear_mind:
        if random.randint(1,100) <= clear_mind_percentage:
            bonus_empower +=5
    if dmg_ring:
        bonus_empower += 4.9
    bonus_empower -= random.randint(0,40) # random weakens
    
    if bonus_empower > 50:
        return 1.5
    elif bonus_empower < -50:
        return 0.5
    return round(1 + bonus_empower/100,2)

def dmg_absorbed(old_fort_percentage):
    return (100-old_fort_percentage)/100

def fort_percentage(target_weight,shirking=False,shirking_uptime=50,shirking_amount=5,fort_amt=0,con_200=True):
    bonus_weight_percentage = 0

    if shirking:
        if random.randint(1,100) <= shirking_uptime:
            fort_amt += 4.9*shirking_amount

    scaling_factor = {
        "heavy": 1.05,
        "medium": 1.04,
        "light": 1.022,
    }

    balanced_armor_value = {
        "heavy": 1887.4,
        "medium": 1382.8,
        "light": 762
    }

    if con_200:
        bonus_weight_percentage += 10

    bonus_weight_factor = (100 + bonus_weight_percentage)/100
    fort_percentage = (100 + fort_amt)/100

    base_ehp = 1+(scaling_factor[target_weight]+balanced_armor_value[target_weight]*bonus_weight_factor)/625**1.2
    fort_amt = 1+(scaling_factor[target_weight]+balanced_armor_value[target_weight]*bonus_weight_factor*fort_percentage)/625**1.2

    return round(base_ehp/fort_amt,2)

def calc_dmg(nw_class,amt_resil_ui=0,amt_shirking_ui=0,amt_aversion_ui=0):
    if nw_class == "med_bruiser_ga":
        crit_out = crit(base_crit=7,backstab_percent=22.5,keen_awareness=True)
        crit_dmg_out = crit_dmg(crit_dmg=30,con_150=True,bonus_crit_dmg=10,amt_resil=amt_resil_ui)
        base_dmg_out = base_dmg(1250,crit=crit_out,crit_dmg=crit_dmg_out,weight_class="medium",aversion=False,thwarting=True,attunement=True,str_50=True,str_100=True,str_200=True)
        empower_percentage_out = empower_percentage(keenly_empowered=False,greed=True,center_of_attention=True)
        dmg_absorbed_out = dmg_absorbed(15)
        fort_percentage_out = fort_percentage(target_weight="medium",shirking=True,shirking_amount=amt_shirking_ui,fort_amt=random.randint(-50,50),con_200=True)

        damage = base_dmg_out * empower_percentage_out * dmg_absorbed_out * fort_percentage_out

        return [round(damage),base_dmg_out,crit_out,crit_dmg_out,empower_percentage_out,dmg_absorbed_out,fort_percentage_out]

    if nw_class == "med_bruiser_ga_emp":
        crit_out = crit(base_crit=7,backstab_percent=22.5,keen_awareness=True)
        crit_dmg_out = crit_dmg(crit_dmg=30,con_150=True,bonus_crit_dmg=10,amt_resil=amt_resil_ui)
        base_dmg_out = base_dmg(1250,crit=crit_out,crit_dmg=crit_dmg_out,weight_class="medium",aversion=False,thwarting=True,attunement=True,str_50=True,str_100=True,str_200=True)
        empower_percentage_out = empower_percentage(keenly_empowered=False,greed=True,center_of_attention=True,shirking_empower=True)
        dmg_absorbed_out = dmg_absorbed(15)
        fort_percentage_out = fort_percentage(target_weight="medium",shirking=True,shirking_amount=amt_shirking_ui,fort_amt=random.randint(-50,50),con_200=True)

        damage = base_dmg_out * empower_percentage_out * dmg_absorbed_out * fort_percentage_out

        return [round(damage),base_dmg_out,crit_out,crit_dmg_out,empower_percentage_out,dmg_absorbed_out,fort_percentage_out]

    elif nw_class == "med_bruiser_wh_shirk":
        crit_out = crit(base_crit=7,backstab_percent=35,keen_awareness=True)
        crit_dmg_out = crit_dmg(crit_dmg=20,con_150=True,bonus_crit_dmg=0,amt_resil=amt_resil_ui)
        base_dmg_out = base_dmg(1250,crit=crit_out,crit_dmg=crit_dmg_out,weight_class="medium",aversion=False,thwarting=True,shirking=True,str_50=True,str_100=True,str_200=True)
        empower_percentage_out = empower_percentage(keenly_empowered=False,power_through_pain=True,shirking_empower=True)
        dmg_absorbed_out = dmg_absorbed(5)
        fort_percentage_out = fort_percentage(target_weight="medium",shirking=True,shirking_amount=amt_shirking_ui,fort_amt=random.randint(-50,50),con_200=True)

        damage = base_dmg_out * empower_percentage_out * dmg_absorbed_out * fort_percentage_out

        return [round(damage),base_dmg_out,crit_out,crit_dmg_out,empower_percentage_out,dmg_absorbed_out,fort_percentage_out]
   
    elif nw_class == "med_bruiser_wh_attunement":
        crit_out = crit(base_crit=7,backstab_percent=35,keen_awareness=True)
        crit_dmg_out = crit_dmg(crit_dmg=20,con_150=True,bonus_crit_dmg=0,amt_resil=amt_resil_ui)
        base_dmg_out = base_dmg(1250,crit=crit_out,crit_dmg=crit_dmg_out,weight_class="medium",aversion=False,thwarting=True,attunement=True,str_50=True,str_100=True,str_200=True)
        empower_percentage_out = empower_percentage(keenly_empowered=False,power_through_pain=True)
        dmg_absorbed_out = dmg_absorbed(5)
        fort_percentage_out = fort_percentage(target_weight="medium",shirking=True,shirking_amount=amt_shirking_ui,fort_amt=random.randint(-50,50),con_200=True)

        damage = base_dmg_out * empower_percentage_out * dmg_absorbed_out * fort_percentage_out

        return [round(damage),base_dmg_out,crit_out,crit_dmg_out,empower_percentage_out,dmg_absorbed_out,fort_percentage_out]
    
    elif nw_class == "light_fs_vicious":
        crit_out = crit(base_crit=10,spellslinger=True,keen_awareness=True)
        crit_dmg_out = crit_dmg(crit_dmg=35,int_50=True,con_150=True,bonus_crit_dmg=12,prophet_of_a_fire_god=True,amt_resil=amt_resil_ui) # includes vicious
        base_dmg_out = base_dmg(1250,crit=crit_out,crit_dmg=crit_dmg_out,weight_class="light",int_300=True,aversion=True,aversion_amt=amt_aversion_ui,attunement=True,int_150=True)
        empower_percentage_out = empower_percentage(keenly_empowered=True,clear_casting=True,clear_mind=True)
        dmg_absorbed_out = dmg_absorbed(15)
        fort_percentage_out = fort_percentage(target_weight="medium",shirking=True,shirking_amount=amt_shirking_ui,fort_amt=random.randint(-50,50),con_200=True)

        damage = base_dmg_out * empower_percentage_out * dmg_absorbed_out * fort_percentage_out
        
        return [round(damage),base_dmg_out,crit_out,crit_dmg_out,empower_percentage_out,dmg_absorbed_out,fort_percentage_out]
    
    elif nw_class == "light_fs_vicious_fire_damage":
        crit_out = crit(base_crit=10,spellslinger=True,keen_awareness=False)
        crit_dmg_out = crit_dmg(crit_dmg=35,int_50=True,con_150=True,bonus_crit_dmg=12,prophet_of_a_fire_god=True,amt_resil=amt_resil_ui) # includes vicious
        base_dmg_out = base_dmg(1250,crit=crit_out,crit_dmg=crit_dmg_out,weight_class="light",int_300=True,aversion=True,aversion_amt=amt_aversion_ui,attunement=True,int_150=True,invig_punishment=True)
        empower_percentage_out = empower_percentage(keenly_empowered=True,clear_casting=True,clear_mind=True,dmg_ring=True)
        dmg_absorbed_out = dmg_absorbed(15)
        fort_percentage_out = fort_percentage(target_weight="medium",shirking=True,shirking_amount=amt_shirking_ui,fort_amt=random.randint(-50,50),con_200=True)

        damage = base_dmg_out * empower_percentage_out * dmg_absorbed_out * fort_percentage_out
        
        return [round(damage),base_dmg_out,crit_out,crit_dmg_out,empower_percentage_out,dmg_absorbed_out,fort_percentage_out]
    
    elif nw_class == "light_fs_vicious_keen":
        crit_out = crit(base_crit=10,spellslinger=True,keen_awareness=True)
        crit_dmg_out = crit_dmg(crit_dmg=35,int_50=True,con_150=True,bonus_crit_dmg=12,prophet_of_a_fire_god=True,amt_resil=amt_resil_ui) # includes vicious
        base_dmg_out = base_dmg(1250,crit=crit_out,crit_dmg=crit_dmg_out,weight_class="light",int_300=True,aversion=True,aversion_amt=amt_aversion_ui,attunement=True,int_150=True,invig_punishment=True)
        empower_percentage_out = empower_percentage(keenly_empowered=True,clear_casting=True,clear_mind=True,dmg_ring=False)
        dmg_absorbed_out = dmg_absorbed(15)
        fort_percentage_out = fort_percentage(target_weight="medium",shirking=True,shirking_amount=amt_shirking_ui,fort_amt=random.randint(-50,50),con_200=True)

        damage = base_dmg_out * empower_percentage_out * dmg_absorbed_out * fort_percentage_out
        
        return [round(damage),base_dmg_out,crit_out,crit_dmg_out,empower_percentage_out,dmg_absorbed_out,fort_percentage_out]

    elif nw_class == "light_fs_vicious_keen_dmg":
        crit_out = crit(base_crit=10,spellslinger=True,keen_awareness=True)
        crit_dmg_out = crit_dmg(crit_dmg=35,int_50=True,con_150=True,bonus_crit_dmg=12,prophet_of_a_fire_god=True,amt_resil=amt_resil_ui) # includes vicious
        base_dmg_out = base_dmg(1250,crit=crit_out,crit_dmg=crit_dmg_out,weight_class="light",int_300=True,aversion=True,aversion_amt=amt_aversion_ui,attunement=True,int_150=True,invig_punishment=False)
        empower_percentage_out = empower_percentage(keenly_empowered=True,clear_casting=True,clear_mind=True,dmg_ring=False)
        dmg_absorbed_out = dmg_absorbed(15)
        fort_percentage_out = fort_percentage(target_weight="medium",shirking=True,shirking_amount=amt_shirking_ui,fort_amt=random.randint(-50,50),con_200=True)

        damage = base_dmg_out * empower_percentage_out * dmg_absorbed_out * fort_percentage_out
        
        return [round(damage),base_dmg_out,crit_out,crit_dmg_out,empower_percentage_out,dmg_absorbed_out,fort_percentage_out]
# calc_dmg("light_fs")
# calc_dmg("med_bruiser_ga")