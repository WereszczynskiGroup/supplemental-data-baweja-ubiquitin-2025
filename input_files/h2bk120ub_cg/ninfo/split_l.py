#!/usr/bin/python3

import sys

filename = sys.argv[1]
num_units = 10

parameter = ["bond",
            "angl",
            "aicg13",
            "dihd",
            "aicgdih",
            "contact"]

headerCheck = ["<<<< native bond length",
              "<<<< native bond angles",
              "<<<< 1-3 contacts",
              "<<<< native dihedral angles",
              "<<<< <<<< 1-4 contacts",
              "<<<< native contact"]

header = ["<<<< native bond length\n** coef_bd(kcal/mol) = factor_bd * correct_bd_mgo * cbd * energy_unit_protein\n**      ibd iunit1-iunit2   imp1 - imp2 imp1un-imp2un      bd_nat    factor_bd  correct_mgo      coef_bd\n",
         "<<<< native bond angles\n** coef_ba(kcal/mol) = factor_ba * correct_ba_mgo * cba * energy_unit_protein\n**      iba iunit1-iunit2   imp1 - imp2 - imp3 imp1un-imp2un-imp3un      ba_nat    factor_ba  correct_mgo      coef_ba\n",
         "<<<< 1-3 contacts with L_AICG2 or L_AICG2_PLUS\n** coef_aicg13_gauss(kcal/mol) = factor_aicg13 * correct_ba_mgo * coef_aicg13_gauss * energy_unit_protein\n**      iba iunit1-iunit2   imp1 - imp2 - imp3 imp1un-imp2un-imp3un  aicg13_nat  factor_aicg13  correct_mgo  coef_aicg13_gauss wid_aicg13_gauss\n",
         "<<<< native dihedral angles \n** coef_dih1(kcal/mol) = factor_dih * correct_dih_mgo * cdih_1 * energy_unit_protein\n** coef_dih3(kcal/mol) = factor_dih * correct_dih_mgo * cdih_3 * energy_unit_protein\n**     idih iunit1-iunit2   imp1 - imp2 - imp3 - imp4 imp1un-imp2un-imp3un-imp4un      dih_nat   factor_dih  correct_mgo   coef_dih_1   coef_dih_3\n",
         "<<<< <<<< 1-4 contacts with L_AICG2_PLUS\n** coef_dih_gauss(kcal/mol) = factor_aicg14 * correct_dih_mgo * coef_aicg14(kcal/mol) * energy_unit_protein\n**     idih iunit1-iunit2   imp1 - imp2 - imp3 - imp4 imp1un-imp2un-imp3un-imp4un   dih_nat factor_aicg14  correct_mgo  coef_dih_gauss  wid_dih_gauss\n",
         "<<<< native contact\n** total_contact =   3900\n** definition_of_contact =       6.50 A\n** coef_go(kcal/mol) = factor_go * icon_dummy_mgo * cgo1210 * energy_unit_protein\n\n** contact between unit      1 and      1\n** total_contact_unit =    259\n**        icon iunit1-iunit2   imp1 - imp2 imp1un-imp2un      go_nat   factor_go  dummy     coef_go\n"]



for i in range(1, num_units+1):
    with open(filename, "r") as f:
        fp = open("unit" + str(i)+"-"+str(i) +".ninfo", "w")
        for line in f:
            for j in range(len(parameter)):
                if line.startswith(headerCheck[j]):
                    fp.write(header[j])
                if (line.startswith(parameter[j]) and line.split()[2] == str(i) and line.split()[2] == line.split()[3]):
                    fp.writelines("%s" % line)
                if (line.startswith(">>>>") and j == int(len(parameter) - 1)):
                    fp.write(">>>>\n\n")
        fp.close()
