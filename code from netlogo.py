# breed [residentials residential]
# breed [commercials commercial]
# breed [companies company]
# breed [powerplants powerplant]
#
# globals [
#   total-consumption
#   total-clean-demand
#   total-generation
#   total-clean-gen
#   CO2-usage
#   average-bill-residential
#   average-bill-commercial
#   average-consumption-residential
#   average-consumption-commercial
#   scale
#   total-capacity
#   total-clean-capacity
#   residential-kWh-cost
#   commercial-kWh-cost
#   total-kWh-cost
#   d ;Discount rate
#   d-solar
#   d-wind
#
#   nuclear-plantsize
#   coal-plantsize
#   gas-plantsize
#   wind-plantsize
#   solar-plantsize
#   cost-list
#   clean-cost-list
#   optimal-gen-cost
#   optimal-gen-source
#   optimal-renewable-cost
#   optimal-renewable-type
#   low-cost
#
#   res-factor
#   res-growth
#   com-factor
#   com-growth
#
#   nuclear
#   coal
#   gas
#   solar
#   wind
#
#   nuclear-CRF ; Capital Recovery Factor
#   nuclear-capacity ;Amount of generation energy
#   nuclear-generation
#   nuclear-CO2 ;Kilograms of CO2 released per MW
#   ;nuclear-employment
#   nuclear-cost
#    nuclear-plantlife
#    nuclear-efficiency
#    nuclear-capitalcost
#    nuclear-operationscost
#    nuclear-variablecost
#    nuclear-fuelcost
#    nuclear-heatrate
#
#   coal-CRF
#   coal-capacity
#   coal-generation
#   coal-employment
#   coal-CO2
#   coal-cost
#    coal-plantlife
#    coal-efficiency
#    coal-capitalcost
#    coal-operationscost
#    coal-variablecost
#    coal-fuelcost
#    coal-heatrate
#
#   gas-CRF
#   gas-capacity
#   gas-generation
#   gas-employment
#   gas-CO2
#   gas-cost
#    gas-plantlife
#    gas-efficiency
#    gas-capitalcost
#    gas-operationscost
#    gas-variablecost
#    gas-fuelcost
#    gas-heatrate
#
#   solar-CRF
#   solar-CO2
#   solar-capacity
#   solar-generation
#   solar-employment
#   solar-cost
#    solar-plantlife
#    solar-efficiency
#    solar-capitalcost
#    solar-operationscost
#
#   wind-CRF
#   wind-CO2
#   wind-capacity
#   wind-generation
#   wind-employment
#   wind-cost
#    wind-plantlife
#    wind-efficiency
#    wind-capitalcost
#    wind-operationscost
#
#   hydro-capacity
#   hydro-generation
#   hydro-cost
#   hydro-CO2
#   hydro-efficiency
# ]
#
# residentials-own [
#   money ;INCOME; How much money they make each tick, to be put into savings + pay for bill
#   savings ;WEALTH; How much money they have saved up to increase their energy efficiency
#   energy-usage ; How much energy the house uses this tick
#   costs ; How much the house is paying for their energy needs (53% factor)
#   WTP ; How aware the household is of environmental impacts and how Willing they are to Pay for renewable
#       ; "Concerned" = $29 (39%), "Protest" = $13 (17%), "Willing" = $36 (26%), "Unwilling" = $0 (18%) /per quarter
#   cost-conscious ;A factor percentage of how important cost is for a household
#   has-solar?
#   has-clean?
# ]
#
# commercials-own [
#   money ;How much money they make each tick, to be put into savings + pay for bill
#   savings ;How much money they have saved up to increase their energy efficiency
#   energy-usage ; How much energy the building uses this tick
#   costs ; How much the house is paying for their energy needs
#   WTP ; How aware the household is of environmental impacts and how Willing they are to Pay for renewable
#       ; "Concerned" = $29 (39%), "Protest" = $13 (17%), "Willing" = $36 (26%), "Unwilling" = $0 (18%) /per quarter
#   cost-conscious ;A factor percentage of how important cost is for a household
#   has-solar?
#   has-clean?
# ]
#
# powerplants-own [
#   power ;What kind of energy this plant produces
#   capacity ;How big the plant is
#   months-running ;How long the plant has been running
# ]
#
# to setup
#   clear-all
#   set-default-shape turtles "house"
#
#   ;Through NJ census calculations and https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_08
#   create-residentials (Agents * .87) [setxy random-xcor random-ycor]
#   create-commercials (Agents * .13) [setxy random-xcor random-ycor]
#
#   ask residentials [set size .4]
#   ask residentials [set color green]
#   ask commercials [set color blue]
#   reset-ticks
#
#   set-scale
#   setup-values
#   setup-prices
#   setup-CO2
#   setup-capacity
#   setup-kWh-cost
#   set-resident
#   set-commercial
# end
#
# to setup-values
#
#   ; Using Market Levelizing Mode and Looking at the Levelizing Parameters on the Left: http://en.openei.org/apps/TCDB/#blank
#   set d (.07) ;default
#   set d-wind (.057)
#   set d-solar (.1)
#
#   ;http://en.openei.org/apps/TCDB/#blank , https://www.eia.gov/outlooks/capitalcost/pdf/updated_capcost.pdf , and https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capcost_assumption.pdf
#   ;These three websites were used for the values on each of the power plants below.
#   set nuclear-plantlife int(random-normal 60 4)
#   set nuclear-efficiency ((85 + random 10) / 100)
#   set nuclear-capitalcost (5530)
#   set nuclear-operationscost (93.28)
#   set nuclear-variablecost (2.14)
#   set nuclear-fuelcost (0.76)
#   set nuclear-heatrate (10450)
#
#   set coal-plantlife int(random-normal 52 4)
#   set coal-efficiency ((50 + random 5) / 100)
#   set coal-capitalcost (5227)
#   set coal-operationscost (80.53)
#   set coal-variablecost (9.51)
#   set coal-fuelcost (2.34)
#   set coal-heatrate (random-normal 10557 1050)
#
#   set gas-plantlife int(random-normal 45 4)
#   set gas-efficiency ((43 + random 5) / 100)
#   set gas-capitalcost (1200)
#   set gas-operationscost (10.17)
#   set gas-variablecost (2.60)
#   set gas-fuelcost (4.40)
#   set gas-heatrate (random-normal 6989 478)
#
#   set solar-plantlife int(18 + random 5)
#   set solar-efficiency ((14 + random 4)/ 100)
#   set solar-capitalcost (2524)
#   set solar-operationscost (27.75)
#
#   set wind-plantlife int(18 + random 5)
#   set wind-efficiency ((35 + random 6) / 100)
#   set wind-capitalcost (1686)
#   set wind-operationscost (46.71)
#
#   set hydro-cost (0.85)
#   set hydro-efficiency (0.5) ;Google search...
# end
#
# to setup-prices
#   ;Using the formulas from http://en.openei.org/apps/TCDB/levelized_cost_calculations.html
#
#   set nuclear-CRF ((d * (1 + d)^(nuclear-plantlife)) / ((1 + d)^(nuclear-plantlife) - 1))
#   set coal-CRF ((d * (1 + d)^(coal-plantlife)) / ((1 + d)^(coal-plantlife) - 1))
#   set gas-CRF ((d * (1 + d)^(gas-plantlife)) / ((1 + d)^(gas-plantlife) - 1))
#   set solar-CRF ((d-solar * (1 + d-solar)^(solar-plantlife)) / ((1 + d-solar)^(solar-plantlife) - 1))
#   set wind-CRF ((d-wind * (1 + d-wind)^(wind-plantlife)) / ((1 + d-wind)^(wind-plantlife) - 1))
#
#   set nuclear-cost ((nuclear-capitalcost * nuclear-CRF)/(8760 * nuclear-efficiency) +
#     (nuclear-operationscost)/(8760 * nuclear-efficiency) +
#     (nuclear-variablecost)/(1000) +
#     (nuclear-fuelcost * nuclear-heatrate)/(1000000))
#
#   set coal-cost ((coal-capitalcost * coal-CRF)/(8760 * coal-efficiency) +
#     (coal-operationscost)/(8760 * coal-efficiency) +
#     (coal-variablecost)/(1000) +
#     (coal-fuelcost * coal-heatrate)/(1000000))
#
#   set gas-cost ((gas-capitalcost * gas-CRF)/(8760 * gas-efficiency) +
#     (gas-operationscost)/(8760 * gas-efficiency) +
#     (gas-variablecost)/(1000) +
#     (gas-fuelcost * gas-heatrate)/(1000000))
#
#   set solar-cost ((solar-capitalcost * solar-CRF)/(8760 * solar-efficiency) +
#     (solar-operationscost)/(8760 * solar-efficiency))
#
#   set wind-cost ((wind-capitalcost * wind-CRF)/(8760 * wind-efficiency) +
#     (wind-operationscost)/(8760 * wind-efficiency))
#
#   ;ADDED THIS IN TO INCREASE THE INITIAL COST OF RENEWABLES DUE TO STORAGE/RELIABILITY NEEDS:
#   set solar-cost (solar-cost * 1.5)
#   set wind-cost (wind-cost * 1.5)
# end
#
# to setup-capacity ;Numbers are in MW
#   set nuclear-plantsize 1100
#   set coal-plantsize 400
#   set gas-plantsize 800
#   set wind-plantsize 1.5
#   set solar-plantsize 14
#
#   ;Nuclear. Values from https://en.wikipedia.org/wiki/List_of_power_stations_in_New_Jersey
#   create-powerplants 1 [
#     set power ("nuclear")
#       set capacity (1268) ;MW
#       set months-running (372)
#   ]
#   create-powerplants 1 [
#     set power ("nuclear")
#     set capacity (636) ;MW
#     set months-running (570)
#   ]
#   create-powerplants 1 [
#     set power ("nuclear")
#     set capacity (1174) ;MW
#     set months-running (479)
#   ]
#   create-powerplants 1 [
#     set power ("nuclear")
#     set capacity (1130) ;MW
#     set months-running (434)
#   ]
#
#   ;Natural Gas has been split between big and small factories to lower variance.
#   ;Numbers based off of PSEG capacity MW values: https://www.pseg.com/family/power/generation.jsp
#   ;Months from Net Generation Capacity Additions: https://energy.gov/sites/prod/files/2017/01/f34/QER%20Transforming%20the%20Nations%20Electricity%20System%20Full%20Report.pdf
#   ;Generation Capacity Age is on Page 1-21 of above link
#   create-powerplants 12 [
#    set power ("gas")
#    set capacity (random-normal 578 426)
#    set months-running (random-normal 186 54)
#   ]
#   create-powerplants 4 [
#    set power ("gas")
#    set capacity (random-normal 1397 168.5)
#    set months-running (random-normal 186 54)
#   ]
#
# ;Coal Capacity
# ;Values based off of PSEG capacity MW values: https://www.pseg.com/family/power/generation.jsp
# ;Months from Net Generation Capacity Additions: https://energy.gov/sites/prod/files/2017/01/f34/QER%20Transforming%20the%20Nations%20Electricity%20System%20Full%20Report.pdf
# ;Generation Capacity Age is on Page 1-21 of above link
#   create-powerplants 4 [
#    set power ("coal")
#    set capacity (random-normal 392 7)
#    set months-running (random-normal 480 60)
#   ]
#
# ;Wind Capacity
# ;Jersey-Atlantic Wind Farm has 5 1.5 MW units running since March, 2006.
#   create-powerplants 5 [
#     set power ("wind")
#     set capacity (1.5)
#     set months-running (127)
#    ]
#
#   ;Solar Capacity
#   ;According to: https://en.wikipedia.org/wiki/Solar_power_in_New_Jersey solar capacity falls between 8 and 20 megawatts.
#   ;Months from Net Generation Capacity Additions: https://energy.gov/sites/prod/files/2017/01/f34/QER%20Transforming%20the%20Nations%20Electricity%20System%20Full%20Report.pdf
#   ;Generation Capacity Age is on Page 1-21 of above link
#   create-powerplants 106 [
#     set power ("solar")
#     set capacity (random-normal 14 4)
#     set months-running (random-normal 3 1)
#   ]
#
#   ;Hydro Capacity
#   create-powerplants 1 [
#     set power ("hydro")
#     set capacity (0)
#     set months-running (0)
#   ]
#
#   ;Hides from map
#   ask powerplants[set size 0]
#
#   ;Inserts values into global variable for easier manipulation
#   set nuclear-capacity (sum [capacity] of powerplants with [power = "nuclear"])
#   set coal-capacity (sum [capacity] of powerplants with [power = "coal"])
#   set gas-capacity (sum [capacity] of powerplants with [power = "gas"])
#   set wind-capacity (sum [capacity] of powerplants with [power = "wind"])
#   set solar-capacity (sum [capacity] of powerplants with [power = "solar"])
#   set hydro-capacity (sum [capacity] of powerplants with [power = "hydro"])
#
#   set total-capacity (nuclear-capacity + coal-capacity + gas-capacity + wind-capacity + solar-capacity)
#   set total-clean-capacity (wind-capacity + solar-capacity)
#
#   ;Converts from MW to MWh
#   ;Total generation is found by multiplying: capacity * hours in a day * average days in a month(30.416) * efficiency
#   ;Gas * .12 is used to mimic Combustion Turbines which are less efficient than combined-cycle
#   set nuclear-generation (nuclear-capacity * 24 * 30.416 * nuclear-efficiency)
#   set coal-generation (coal-capacity * 24 * 30.416 * coal-efficiency)
#   set gas-generation ((gas-capacity * 24 * 30.416 * gas-efficiency * .8) + (gas-capacity * 24 * 30.416 * .12 * .2))
#   set wind-generation (wind-capacity * 18 * 30.416 * wind-efficiency)
#   set solar-generation (solar-capacity * 12 * 30.416 * solar-efficiency)
#   set hydro-generation (hydro-capacity * 24 * 30.416 * hydro-efficiency)
#
# ;  set nuclear-generation (nuclear-capacity * 24 * 30.416)
# ;  set coal-generation (coal-capacity * 24 * 30.416)
# ;  set gas-generation (gas-capacity * 24 * 30.416)
# ;  set wind-generation (wind-capacity * 18 * 30.416)
# ;  set solar-generation (solar-capacity * 12 * 30.416)
# ;  set hydro-generation (hydro-capacity * 24 * 30.416)
#
#   set total-clean-gen (wind-generation + solar-generation + hydro-generation)
#   set total-generation (total-clean-gen + nuclear-generation + coal-generation + gas-generation)
# end
#
# to setup-CO2
#   ;http://en.openei.org/apps/LCA/
#   set wind-CO2 (12) ;kilograms per MWh
#   set solar-CO2 (54)
#   set nuclear-CO2 (12)
#   set gas-CO2 (477)
#   set coal-CO2 (1001)
#   set hydro-CO2 (8)
# end
#
# to-report  log-normal [#mu #sigma]
#   let beta ln (1 + ((#sigma ^ 2) / (#mu ^ 2)))
#   let x exp (random-normal (ln (#mu) - (beta / 2)) sqrt beta)
#   report x
# end
#
# to set-resident
#   ask residentials [set WTP (random-normal 16 16)]
# ;  ask residentials [if WTP < 0 [set WTP 0]]
#    ;May need to lower because numbers are much larger in Europe/Australia
#   ask residentials [set energy-usage (random-normal 696 100)]
#   ask residentials [set savings (log-normal 700000 700000)]  ;2010 Census data say 72.4% white, 12.6% black, 16.3% Latino; 2016 Fed survey says mean wealth $934k white, $138k black, $191k hispanic: https://www.federalreserve.gov/econres/notes/feds-notes/recent-trends-in-wealth-holding-by-race-and-ethnicity-evidence-from-the-survey-of-consumer-finances-20170927.htm
# ;  ask residentials [set cost-conscious (((random-normal 100 12) / 100) ^ -1)]  ;THIS IS NOT USED!
#   ask residentials [set costs (energy-usage * residential-kWh-cost)]
#   ask residentials [set money (log-normal 75000 25000)]
#   ask residentials [set has-solar? 0]
#   ask residentials [set has-clean? 0]
# end
#
# to set-commercial
#   ask commercials [set WTP (random-normal 200 200)]
# ;  ask commercials [if WTP < 0 [set WTP 0]]
#    ;May need to lower because numbers are much larger in Europe/Australia
#   ask commercials [set energy-usage (random-normal 6300 1000)]
#   ask commercials [set savings (log-normal 3000000 1000000)]
# ;  ask commercials [set cost-conscious (((random-normal 110 12) / 100) ^ -1)]
#   ask commercials [set costs (energy-usage * commercial-kWh-cost)]
#   ask commercials [set money (log-normal 300000 150000)]
#   ask commercials [set has-solar? 0]
#   ask commercials [set has-clean? 0]
# end
#
# to set-scale
#   ;sets a scale to be used later so that one agent represents enough buildings to consider all of NJ's housing.
#   set scale (4000000 / Agents) ;assumes 4M households in NJ (though 2010 Census shows 3.2M)
# end
#
# to setup-kWh-cost
#   ;1.8 and 1.5 multiples are used to account for distribution charges. EIA.gov explains around ~57% of charges are generation.
#   ;https://www.eia.gov/energyexplained/index.cfm?page=electricity_factors_affecting_prices
#   set residential-kWh-cost 1.8 * ((nuclear-capacity * nuclear-cost) + (coal-capacity * coal-cost) + (gas-capacity * gas-cost) + (wind-capacity * wind-cost) + (solar-capacity * solar-cost)) / total-capacity
#   set commercial-kWh-cost 1.5 * ((nuclear-capacity * nuclear-cost) + (coal-capacity * coal-cost) + (gas-capacity * gas-cost) + (wind-capacity * wind-cost) + (solar-capacity * solar-cost)) / total-capacity
#   set total-kWh-cost residential-kWh-cost + commercial-kWh-cost
# end
#
# to change-prices
#
#   ;https://www.eia.gov/outlooks/capitalcost/pdf/updated_capcost.pdf , and https://www.eia.gov/analysis/studies/powerplants/capitalcost/pdf/capcost_assumption.pdf
#   ;These two websites were compared of differences between both years. Values were divided by 12 to account for months (That's why some values are very small).
#   set nuclear-plantlife (nuclear-plantlife + random-float .01)
#   set solar-plantlife (solar-plantlife + random-float .16)
#   set wind-plantlife (wind-plantlife + random-float .033)
#   set gas-plantlife (gas-plantlife + random-float .016)
#   set coal-plantlife (coal-plantlife + random-float .016)
#
#   set nuclear-capitalcost (nuclear-capitalcost + random-float 10.52)
#   set wind-capitalcost (wind-capitalcost + random-float 8.33)
#   set solar-capitalcost (solar-capitalcost - random-float 3)
#   set gas-capitalcost (gas-capitalcost + random-float 1.69)
#   set coal-capitalcost (coal-capitalcost + random-float 5.5)
#
#   set nuclear-operationscost (nuclear-operationscost + random-normal .2 .05)
#   set gas-operationscost (gas-operationscost + random-normal .003 .002)
#   set coal-operationscost (coal-operationscost + random-normal .1 .05)
#   set wind-operationscost (wind-operationscost + random-normal .004 .002)
#   set solar-operationscost (solar-operationscost - random-normal .08 .03)
#
#   set nuclear-variablecost (nuclear-variablecost + random-normal .0044 .002)
#   set gas-variablecost (gas-variablecost + random-normal .0028 .0015)
#   set coal-variablecost (coal-variablecost + random-normal .0035 .002)
#
#   set coal-efficiency (coal-efficiency + random-float .001)
#   set gas-efficiency (gas-efficiency + random-float (.001 * (1 - wind-investment) / 100))
#   set wind-efficiency (wind-efficiency + random-float (.002 * wind-investment / 100))   ;modified!!!
#   set solar-efficiency (solar-efficiency + random-float .002)
#   set nuclear-efficiency (nuclear-efficiency + random-float .0005)
#
#   set gas-fuelcost (gas-fuelcost + random-normal .013 .007)
#   set coal-fuelcost (coal-fuelcost + random-normal .013 .007)
# end
#
# to plot-data
#   set total-consumption  (((sum [energy-usage] of residentials) + (sum [energy-usage] of commercials)) * scale) / 1000; MWh
#   set total-clean-demand (((sum [has-clean? * energy-usage] of residentials) + (sum [has-clean? * energy-usage] of commercials))* scale) / 1000
#   set average-consumption-residential (sum [energy-usage] of residentials) / (3480000 + (ticks * 2125)) ; Average kWh consumed
#   set average-consumption-commercial (sum [energy-usage] of commercials) / (520000 + (ticks * 229)) ; Average kWh consumed
# ;  set average-bill-residential (sum [costs] of residentials) / (3480000 + (ticks * 2125)) ; Price per kWh -- ASK MARCIN
#   set average-bill-residential ((sum [costs] of residentials)/(count residentials))
# ;  set average-bill-commercial (sum [costs] of commercials) / (520000 + (ticks * 229)) ; Price per kWh -- ASK MARCIN
#   set average-bill-commercial ((sum [costs] of commercials)/(count commercials))
#   set CO2-usage (nuclear-capacity * nuclear-CO2) +
#                 (coal-capacity * coal-CO2) +
#                 (gas-capacity * gas-CO2) +
#                 (wind-capacity * wind-CO2) +
#                 (solar-capacity * solar-CO2)
# end
#
# to population-growth
#   ;Using the last 4 issues of the following link below:
#   ;https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_08
#   ;The mean change in residential and commercial customers was found. This value was divided by 12. The scale was then divided by this number to see how approximately how many months it would take to reach this number.
#   ;Once the number was reached, an extra house, the size of the scale was added.
#   set res-factor (scale / 2000) ;~25504 added residential customers each year / 12 months = 2000
#   if ticks mod (int res-factor) = 0[
#   create-residentials 1 [setxy random-xcor random-ycor
#                          set color green
#                          set size .4
#                          set WTP (random-normal 16 16)
# ;                         if WTP < 0 [set WTP 0]
#                          set energy-usage (random-normal 696 100)
#                          set savings (log-normal 700000 400000)
# ;                         set cost-conscious (((random-normal 100 12) / 100) ^ -1) * scale
#                          set costs (energy-usage * residential-kWh-cost)
#                          set money (log-normal 75000 70000)
#                          set has-clean? 0
#                          set has-solar? 0]]
#
#
#   set com-factor (scale / 229) ;~2743 added commercial customers each year / 12 months = 229.
#   if ticks mod (int com-factor) = 0 [
#   create-commercials 1 [setxy random-xcor random-ycor
#                         set color blue
#                         set WTP (random-normal 200 200)
# ;                        if WTP < 0 [set WTP 0]
#                         set energy-usage (random-normal 6300 1000)
#                         set savings (log-normal 3000000 1000000)
# ;                        set cost-conscious (((random-normal 110 12) / 100) ^ -1) * scale
#                         set costs (energy-usage * commercial-kWh-cost)
#                         set money (log-normal 300000 150000)
#                         set has-clean? 0
#                         set has-solar? 0]]
# end
#
# to change-res
#   ask residentials [set savings (savings + ((money / 80) - costs))]  ;assuming 15% of money goes to utilities or savings
#   ask residentials [set costs (energy-usage * residential-kWh-cost)]
#
#   ask residentials [
#   if (money / 120 - costs) > 0 [
#     set energy-usage (1.001 * energy-usage)
#       if WTP > energy-usage * (0.10 - clean-incentive / 100) [
#         set has-clean? 1]
#   ]]
#   ask residentials[
#   if (money / 120 - costs) < 0 [
#     set energy-usage (0.95 * energy-usage)
#   ]]
#
#   ask commercials [set savings (savings + ((money / 80) - costs))]
#   ask commercials [set costs (energy-usage * commercial-kWh-cost)]
#
#   ask commercials [
#   if (money / 120 - costs) > 0 [
# ;    set energy-usage (1.001 * energy-usage)
#       if WTP > energy-usage * (0.10 - clean-incentive / 100) [
#         set has-clean? 1]
#   ]]
#   ask commercials[
#   if (money / 120 - costs) < 0 [
#     set energy-usage (0.95 * energy-usage)
#   ]]
# end
#
# to retire-capacity
#   ;Updates/Increases Age
#   ask powerplants[set months-running (months-running + 1)]
#
#   ;Checks if Plants are Past Retirement if so, retires the plant
#   ask powerplants with [power = "nuclear"][
#     if months-running > (nuclear-plantlife * 12 ) [die]
#   ]
#   ask powerplants with [power = "coal"][
#     if months-running > (coal-plantlife * 12 ) [die]
#   ]
#   ask powerplants with [power = "gas"][
#     if months-running > (gas-plantlife * 12 ) [die]
#   ]
#   ask powerplants with [power = "solar"][
#     if months-running > (solar-plantlife * 12 ) [die]
#   ]
#   ask powerplants with [power = "wind"][
#     if months-running > (wind-plantlife * 12 ) [die]
#   ]
# end
#
# to recalculate-capacity
#   ;Inserts values into global variable for easier manipulation
#   set nuclear-capacity (sum [capacity] of powerplants with [power = "nuclear"])
#   set coal-capacity (sum [capacity] of powerplants with [power = "coal"])
#   set gas-capacity (sum [capacity] of powerplants with [power = "gas"])
#   set wind-capacity (sum [capacity] of powerplants with [power = "wind"])
#   set solar-capacity (sum [capacity] of powerplants with [power = "solar"])
#   set hydro-capacity (sum [capacity] of powerplants with [power = "hydro"])
#
#   set total-capacity (nuclear-capacity + coal-capacity + gas-capacity + wind-capacity + solar-capacity)
#   set total-clean-capacity (wind-capacity + solar-capacity)
#
#   ;Converts from MW to MWh
#   ;Total generation is found by multiplying: capacity * hours in a day * average days in a month(30.416) * efficiency
#   ;Gas * .12 is used to mimic Combustion Turbines which are less efficient than combined-cycle
#   set nuclear-generation (nuclear-capacity * 24 * 30.416 * nuclear-efficiency)
#   set coal-generation (coal-capacity * 24 * 30.416 * coal-efficiency)
#   set gas-generation ((gas-capacity * 24 * 30.416 * gas-efficiency * .8) + (gas-capacity * 24 * 30.416 * .12 * .2))
#   set wind-generation (wind-capacity * 18 * 30.416 * wind-efficiency)
#   set solar-generation (solar-capacity * 12 * 30.416 * solar-efficiency)
#   set hydro-generation (hydro-capacity * 24 * 30.416 * hydro-efficiency)
#
# ;  set nuclear-generation (nuclear-capacity * 24 * 30.416)
# ;  set coal-generation (coal-capacity * 24 * 30.416)
# ;  set gas-generation (gas-capacity * 24 * 30.416)
# ;  set wind-generation (wind-capacity * 18 * 30.416)
# ;  set solar-generation (solar-capacity * 12 * 30.416)
# ;  set hydro-generation (hydro-capacity * 24 * 30.416)
#
#   set total-clean-gen (wind-generation + solar-generation + hydro-generation)
#   set total-generation (total-clean-gen + nuclear-generation + coal-generation + gas-generation)
#
# ;  set total-clean-gen   (wind-capacity * 18 * 30.416 * wind-efficiency) +
# ;                        (solar-capacity * 12 * 30.416 * solar-efficiency) +
# ;                        (hydro-capacity * 24 * 30.416 * hydro-efficiency) ; MWh
# ;
# ;  set total-generation  (nuclear-capacity * 24 * 30.416 * nuclear-efficiency) +
# ;                        (coal-capacity * 24 * 30.416 * coal-efficiency) +
# ;                        (gas-capacity * 24 * 30.416 * gas-efficiency * .8) +
# ;                        (gas-capacity * 24 * 30.416 * .12 * .2) +
# ;                        total-clean-gen ; MWh
# end
#
# to new-capacity ;NEED TO UPDATE THIS TO CONSIDER POWERPLANT COSTS
#   ;set producer-strategy "wind-only"
#
#   set cost-list (list solar-cost wind-cost gas-cost nuclear-cost coal-cost)
#   set clean-cost-list (list solar-cost wind-cost)
#   set optimal-gen-cost min cost-list
#   set optimal-gen-source position optimal-gen-cost cost-list
#   set optimal-renewable-cost min clean-cost-list
#   set optimal-renewable-type position optimal-renewable-cost clean-cost-list
#
#   ;regardless of strategy, if opt-ins exceed supply, increase the renewable capacity
#   if total-clean-demand > total-clean-gen [
# ;    set optimal-gen-cost min clean-cost-list
# ;    set source-min-cost position optimal-gen-type cost-list
#     if (producer-strategy = ("min-cost")) or (producer-strategy = ("renewable-only")) or (producer-strategy = ("on-demand-only")) [
#       if wind-cost < solar-cost [build-wind]
#       if solar-cost <= wind-cost [build-solar]
#     ]
#     if producer-strategy = ("wind-only") [build-wind]
#     if producer-strategy = ("solar-only") [build-solar]
#   ]
#
#   ;otherwise, increase capacity if demand exceeds capacity
#   if total-clean-demand <= total-clean-gen [
#     if total-generation < (total-consumption * 1.2) [
#       if producer-strategy = ("min-cost") [
#         if optimal-gen-source = 2 [build-gas]
#         if optimal-gen-source = 1 [build-wind]
#         if optimal-gen-source = 0 [build-solar]
#       ]
#
#       if producer-strategy = ("wind-only") [build-wind]
#
#       if producer-strategy = ("solar-only") [build-solar]
#
#       if producer-strategy = ("renewable-only") [
#         if wind-cost < solar-cost [build-wind]
#         if solar-cost <= wind-cost [build-solar]
#       ]
#
#       if producer-strategy = ("on-demand-only") [build-gas]
#       ]
#     ]
# end
#
# to build-wind
#   create-powerplants 75 [
#     set power ("wind")
#     set capacity (1.5)
#     set months-running (0)
#   ]
# end
#
# to build-solar
#   create-powerplants 15 [
#   set power ("solar")
#   set capacity (10)
#   set months-running (0)
#   ]
# end
#
# to build-gas
#   create-powerplants 1 [
#   set power ("gas")
#   set capacity (600)
#   set months-running (0)
#   ]
# end
#
# to go
#   population-growth  ;population expands and new consumer agents are generated
#   change-prices      ;powerplant costs are updated with time/technology
#   setup-prices       ;per unit power costs are updated
#
#   retire-capacity       ;remove aging plants
#   recalculate-capacity  ;recalculate total capacity
#   new-capacity          ;add new plants if capacity is insufficient
#   recalculate-capacity  ;recalculate total capacity
#
#   setup-kWh-cost     ;update prices seen by consumers
#   change-res         ;residential consumers update wealth and energy use choices
#
#   plot-data          ;calculate numbers needed for plots in Interface tab
#   if (ticks >= 480) [stop]   ;stop after 40 years
#   tick               ;advance the time by 1 month
# end
