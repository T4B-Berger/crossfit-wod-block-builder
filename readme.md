# WOD Block Builder

Build a personalized 4-week CrossFit training block from historical WODs.

## Product

WOD Block Builder generates a structured training plan in seconds based on:

- goal (engine, strength, gym, general, weight loss, return to training)
- level (beginner, intermediate, advanced)
- sessions per week (3–5)
- available equipment
- maximum session duration

The output is a **4-week block** with:

- clear progression (base → volume → intensity → deload/test)
- balanced stimulus (engine / strength / gym / mixed)
- detailed sessions
- simple visualizations
- explanation of the programming logic

## Key Idea

This is not a random WOD generator.

It uses a structured dataset of real CrossFit workouts and applies deterministic rules to produce a coherent training block.

## MVP Scope

The MVP focuses on:

- fast generation (<30s perceived)
- clean modern UI (Streamlit)
- credible programming logic
- simple but clear visualizations

Excluded from MVP:

- authentication
- user history
- advanced personalization
- live scraping
- complex backend

## Data

The app relies on a pre-built dataset of parsed WODs including:

- format (AMRAP, for time, EMOM, etc.)
- time domain (short / medium / long)
- focus (engine / strength / gym / mixed)
- equipment requirements
- difficulty score
- movements

## Architecture

- Streamlit → UI
- Python → rule-based programming engine
- CSV dataset → data source
- optional LLM → explanations and warm-ups only

## Vision

Turn a large historical archive of CrossFit workouts into a simple, fast, and credible training block generator.

The goal is to deliver immediate value and a strong “this feels like a coach” effect with minimal friction.
