import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

# Disgusting code

# Paper1 = html.P("1. R. Rivas-Barbosa, M. Escobedo-Sánchez, M. Tassieri, and M. Laurati, “i-Rheo: determining the linear viscoelastic moduli of colloidal dispersions from step-stress measurements”, \
# Phys.Chem.Chem.Phys., 22, 3839 (2020).")

# Paper2 = html.P("2. J.A. Moreno-Guerra, I.C. Romero-Sánchez, A. Martinez-Borquez, M. Tassieri, E. Stiakakis and M. Laurati, “Model free Rheo-AFM probes the viscoelasticity of tunable DNA soft colloids”, \
# Small, (2019), DOI: 10.1002/smll.201904136.")

# Paper3 = html.P("3. M. Tassieri, “Microrheology with Optical Tweezers: Peaks & Troughs”, \
# Curr. Opin. Colloid Interface Sci (2019).")

# Paper4 = html.P("4. L. G. Rizzi and M. Tassieri, “Microrheology of Biological Specimens”, \
# Encyclopedia of Analytical Chemistry: Applications, Theory and Instrumentation (2018).")

# Paper5 = html.P("5. Y. H. Chim, L. M. Mason, N. Rath, M. F. Olson, M. Tassieri & H. Yin, “A one-step procedure to probe the viscoelastic properties of cells by Atomic Force Microscopy”,\
# Scientific Reports, 8, 14462 (2018).")

# Paper6 = html.P("6. M. Tassieri, “Comment on “A symmetrical method to obtain shear moduli from microrheology” by Kengo Nishi, Maria L. Kilfoil, Christoph F. Schmidt, and F. C. MacKintosh, Soft Matter, 2018, 14, 3716”, published as Comment in \
# Soft Matter, 14, 8666 (2018).")

# Paper7 = html.P("7.  M.Tassieri, J.Ramirez, N.Ch.Karayiannis, S.K.SukumaranandY.Masubuchi, “i-RheoGT: Transforming from time- to frequency-domain without artefacts”, \
# Macromolecules, 51, 14, 5055 (2018).")

# Paper8 = html.P("8. M.Tassierietal.,“i-Rheo:Measuringthematerials’linearviscoelasticproperties‘inastep’”, \
# Journal of Rheology, 60, 649 (2016). It has been the \
# 2016's most read article in the Journal of Rheology.")

# Paper9 = html.P("9. Book: “Microrheology with Optical Tweezers: Principles and Applications”, edited by M.Tassieri, June (2016), \
# published by Pan Stanford.")

# Paper10 = html.P("10. M. Tassieri, “Linear Microrheology with Optical Tweezers of living cells ‘is not an option’!”, published as Opinion in \
# Soft Matter, 11, (2015).")

# Paper11 = html.P("11. M. Tassieri et al., “Microrheology with Optical Tweezers: Measuring the relative viscosity of solutions ‘at a glance’”, \
# Scientific Reports, 5, 8831 (2015).")

# Paper12 = html.P("12. M. Tassieri et al., “Microrheology with optical tweezers: data analysis”, \
# New J. of Physics,14, 115032 (2012).")

# Paper13 = html.P("13. D. Preece, R.L. Warren, G.M. Gibson, R.M.L. Evans, M.J. Padgett, J.M. Cooper, and M.Tassieri, “Optical tweezers: wideband microrheology”, \
# J. Optics, 13, 044022 (2011).")

# Paper14 = html.P("14. M. Tassieri et al., “Analysis of the linear viscoelasticity of polyelectrolytes by magnetic microrheometry-Pulsed creep experiments and the one particle response”, \
# J. Rheol., 54, 117(2010).")

# Paper15 = html.P("15. M. Tassieri, G.M. Gibson, R.M.L. Evans, A.M. Yao, R. Warren, M.J. Padgett, and J.M.Cooper “Measuring storage and loss moduli using optical tweezers: broadband microrheology”, \
# Phys. Rev. E, 81, (2010).")

# Paper16 = html.P("16. R.M.L. Evans, M. Tassieri, D. Auhl and T.A. Waigh, “Direct conversion of rheological compliance measurements into storage and loss moduli”, \
# Phys. Rev. E, 80, 012501 (2009).")

# Paper17 = html.P("17. A.M. Yao, M. Tassieri, M.J. Padgett, J.M. Cooper, “Microrheology with optical tweezers”, \
# LoC, 9, 2568 (2009).")

# AllPapers = [
#     Paper1, Paper2, Paper3, Paper4, Paper5, Paper6, Paper7, Paper8,
#     Paper9, Paper10, Paper11, Paper12, Paper13, Paper14, Paper15, Paper16,
#     Paper17, PaperT
# ]
AllPapers = []

PaperMarkDown = dcc.Markdown('''
1. R. Rivas-Barbosa, M. Escobedo-Sánchez, **M. Tassieri**, and M. Laurati, “i-Rheo: determining the linear viscoelastic moduli of colloidal dispersions from step-stress measurements”, Phys.Chem.Chem.Phys., 22, 3839 (2020).

2. J.A. Moreno-Guerra, I.C. Romero-Sánchez, A. Martinez-Borquez, **M. Tassieri**, E. Stiakakis and M. Laurati, “Model free Rheo-AFM probes the viscoelasticity of tunable DNA soft colloids”, Small, (2019), DOI: 10.1002/smll.201904136.

3. **M. Tassieri**, “Microrheology with Optical Tweezers: Peaks & Troughs”, Curr. Opin. Colloid Interface Sci (2019).

4. L. G. Rizzi and **M. Tassieri**, “Microrheology of Biological Specimens”, Encyclopedia of Analytical Chemistry: Applications, Theory and Instrumentation (2018).

5. Y. H. Chim, L. M. Mason, N. Rath, M. F. Olson, **M. Tassieri** & H. Yin, “A one-step procedure to probe the viscoelastic properties of cells by Atomic Force Microscopy”, Scientific Reports, 8, 14462 (2018).

6. **M. Tassieri**, “Comment on “A symmetrical method to obtain shear moduli from microrheology” by Kengo Nishi, Maria L. Kilfoil, Christoph F. Schmidt, and F. C. MacKintosh, Soft Matter, 2018, 14, 3716”, published as Comment in Soft Matter, 14, 8666 (2018).

7. **M. Tassieri**, J.Ramirez, N.Ch.Karayiannis, S.K.Sukumaran and Y.Masubuchi, “i-RheoGT: Transforming from time- to frequency-domain without artefacts”, Macromolecules, 51, 14, 5055 (2018).

8. **M. Tassieri** et al.,“i-Rheo:Measuringthematerials’linearviscoelasticproperties‘inastep’”, Journal of Rheology, 60, 649 (2016). It has been the 2016's most read article in the Journal of Rheology.

9. Book: “Microrheology with Optical Tweezers: Principles and Applications”, edited by **M. Tassieri**, June (2016), published by Pan Stanford.

10. **M. Tassieri**, “Linear Microrheology with Optical Tweezers of living cells ‘is not an option’!”, published as Opinion in Soft Matter, 11, (2015).

11. **M. Tassieri** et al., “Microrheology with Optical Tweezers: Measuring the relative viscosity of solutions ‘at a glance’”, Scientific Reports, 5, 8831 (2015).

12. **M. Tassieri** et al., “Microrheology with optical tweezers: data analysis”, New J. of Physics, 14, 115032 (2012).

13. D. Preece, R.L. Warren, G.M. Gibson, R.M.L. Evans, M.J. Padgett, J.M. Cooper, and **M. Tassieri**, “Optical tweezers: wideband microrheology”, J. Optics, 13, 044022 (2011).

14. **M. Tassieri** et al., “Analysis of the linear viscoelasticity of polyelectrolytes by magnetic microrheometry-Pulsed creep experiments and the one particle response”, J. Rheol., 54, 117(2010).

15. **M. Tassieri**, G.M. Gibson, R.M.L. Evans, A.M. Yao, R. Warren, M.J. Padgett, and J.M. Cooper “Measuring storage and loss moduli using optical tweezers: broadband microrheology”, Phys. Rev. E, 81, (2010).

16. R.M.L. Evans, **M. Tassieri**, D. Auhl and T.A. Waigh, “Direct conversion of rheological compliance measurements into storage and loss moduli”, Phys. Rev. E, 80, 012501 (2009).

17. A.M. Yao, **M. Tassieri**, M.J. Padgett, J.M. Cooper, “Microrheology with optical tweezers”, LoC, 9, 2568 (2009).
''')