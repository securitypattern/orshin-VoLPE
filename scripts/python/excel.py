#=================================================
# Copyright (c) 2025, Security Pattern
# All rights reserved.
#
#    This file is part of: Side-channel leakages analysis with VoLPE.
#
#    SPDX-License-Identifier: MIT 
#=================================================

import pandas as pd

def write_chart(writer, sheet, shape):
    workbook  = writer.book
    worksheet = writer.sheets[sheet]
    chart = workbook.add_chart({'type': 'column'})
    chart.add_series({
        'categories': [sheet, 1, 0, shape[0], 0],
        'values': [sheet, 1, 1, shape[0], 1]
        })
    worksheet.insert_chart(1, 3, chart, {'x_scale': 1.5, 'y_scale': 1.5})

def create_del_df(in_delays, gate_delays):
    in_del = dict()
    gate_del = dict()

    for e in in_delays:
        in_del[e.split()[0]] = e.split()[1]
    in_del_df = pd.DataFrame(data=list(in_del.items()), columns=["Input", "Used delay"])

    for e in gate_delays:
        gate_del[e.split()[0]] = e.split()[1] 
    gate_del_df = pd.DataFrame(data=list(gate_del.items()), columns=["Gate", "Used delay"])

    return in_del_df, gate_del_df

# Write data to excek file
def write_excel(spreadsheet, data, in_delays, gate_delays):
    # data[0] -> correlation matrix
    # data[1] -> data for no del toggle bar chart
    # data[2] -> data for  del toggle bar chart
    # data[3] -> data for in_del toggle bar chart

    with pd.ExcelWriter("./spreadsheets/" + spreadsheet + ".xlsx") as writer:
        # correlation matrix on first sheet
        data[0].to_excel(writer, index=True, sheet_name="Correlation matrix")

        # used delays on first sheet
        in_del_df, gate_del_df = create_del_df(in_delays, gate_delays)
        in_del_df.to_excel(writer, index=False, sheet_name="Correlation matrix", startrow=6)
        gate_del_df.to_excel(writer, index=False, sheet_name="Correlation matrix", startrow=6, startcol=3)

        # no del toggles bar chart
        data[1].to_excel(writer, index=True, sheet_name="Toggles no del")
        #write_chart(writer, "Toggles no del", data[1].shape)

        # no del toggles bar chart
        data[2].to_excel(writer, index=True, sheet_name="Toggles del")
        #write_chart(writer, "Toggles del", data[2].shape)

        # no del toggles bar chart
        data[3].to_excel(writer, index=True, sheet_name="Toggles input del")
        #write_chart(writer, "Toggles input del", data[3].shape)