# Stochastic-analysis-of-blackjack
Stochastic Analysis of Blackjack
================================

This project investigates decision-making in blackjack using Monte Carlo simulation
and statistical analysis of expected values (EVs) under varying deck compositions.

The core idea is to move beyond fixed “basic strategy” rules and instead analyse
how optimal decisions depend on the composition of the remaining deck, in particular
the density of ten-value cards and aces.


⚠️ IMPORTANT
------------

The MAIN result of this project is NOT the source code.

The primary file to read is:

    analysis/analysis_cases.ipynb

This notebook contains:
- all generated datasets
- all visualisations (plots)
- the actual analysis and conclusions

If you only look at one file in this repository, make it this one.


Project Structure
-----------------

analysis/
    analysis_cases.ipynb   ← MAIN FILE (plots + research)
    datasets/              ← generated datasets for different cases

src/
    blackjack/             ← implementation of the blackjack engine
    analysis/              ← Monte Carlo EV estimation logic

test/
    example scripts and logs


What This Project Does
----------------------

- Simulates blackjack using a custom engine
- Estimates expected values (EV) of actions (Hit, Stand, Double, Split)
- Uses Monte Carlo methods with adaptive stopping
- Studies how EV depends on:
    • ten-card density
    • ace density

Rather than analysing random gameplay, the project focuses on
controlled case studies (e.g. "16 vs 10", "8,8 vs 6").


Key Idea
--------

Instead of asking:

    “What is the optimal move?”

we ask:

    “How does the optimal move depend on deck composition?”

This allows us to:
- identify decision boundaries
- explain why basic strategy works
- quantify sensitivity to deck composition


How to Use
-----------

1. Clone the repository
2. Install dependencies (numpy, pandas, matplotlib)
3. Run Jupyter:

    jupyter notebook

4. Open:

    analysis/analysis_cases.ipynb

5. Run all cells


Notes
-----

- The code in /src is designed to support the analysis, not as a standalone product
- The notebook is structured as a research document, not just code execution
- Figures can be exported for use in LaTeX or reports


References & Context
--------------------

Blackjack is a classic stochastic decision problem and is commonly analysed using
simulation or reinforcement learning approaches :contentReference[oaicite:0]{index=0}.
This project follows a Monte Carlo approach, focusing specifically on
composition-dependent effects.


Author
------

Mikhail Aleinikov  
University of Vienna  
Mathematical Foundations of Data Science