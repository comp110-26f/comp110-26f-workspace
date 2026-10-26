# Good Fire — Part 2 (EX06): Plan a Good-Fire Burn (3D)

## The story

You are now on a fire-management team. Your landscape is the one from
Part 1: longleaf pine uplands, hardwoods along the river, an old-field
meadow, a county road, and two neighborhoods where homes meet the woods.

Longleaf pine and wiregrass need fire. They evolved with low-intensity
fire every few years, and without it, brush and hardwoods crowd in and
dead needles pile up into fuel for an intense wildfire. So before the
wildfire season, your team will conduct prescribed fires (**good fires**) on the land. The fire has a job to do, and it has to stay where it
belongs. It should burn the pine and grass, stay out of the bottomland
hardwoods, and above all stay away from homes.

Real burn bosses write a **burn plan** before they light anything:

* **The burn unit**: the area to burn, drawn on a map.
* **The fuels to burn**: here, the pine and the grass.
* **Control lines**: wherever fire could leave those fuels, the crew mows
  or disks a strip down to bare soil. Roads and rivers already stop fire,
  so a smart unit uses them as free *anchors*.
* **A prescription**: the range of weather the burn is allowed in. Too
  damp, and the fire goes out. Too dry or too windy, and embers fly over
  the line.
* **An ignition pattern**: where the crew lights the fire.

You will write the code behind that plan, then choose the best of five
season plans. In the 3D
view, your burn day plays out first. Then months pass, the burned ground
greens up with only a light load of fuel, and the wildfire season begins.
You will see whether your good fire helps protect the homes.

You will plan under two climates. "Historical" weather has a moderate south
breeze over typically damp fuel. "Hotter, drier" weather is the kind a
warming climate makes more common: stronger wind over drought-dry fuel.
That affects both halves of the season. There are fewer calm, damp days
to burn on, and the wildfires that follow are fiercer.

## What you will practice

**Your functions work on plain data.** You never touch the map or the
fire. The provided code turns the map into lists, sets, and dictionaries,
calls your functions, and uses what they return.

* A **kind of land** is a string: `"pine"`, `"grass"`, `"hardwood"`,
  `"home"`, `"water"`, `"road"`, or `"cleared"`.
* A **`Square`** is a label for one place on the map. You never need to
  look inside one. Put `Square`s in sets, use them as dictionary keys, and
  compare them with `==` and `in`. Two `Square`s for the same place are
  equal:

  ```python
  burned: set[Square] = {Square(3, 4), Square(3, 5)}
  Square(3, 4) in burned  # True: a different object, but the same place
  ```

* A **land map** is a `dict[Square, str]`: the kind of land on each
  square.
* A **neighbors map** is a `dict[Square, list[Square]]`: for each square,
  the squares right next to it (north, south, west, and east), where fire
  can spread next.

## The science

Spread follows the cellular-automaton model of Alexandridis et al. (2008):

`chance = P_H * (1 + p_veg) * (1 + p_den) * p_wind * p_slope * p_moisture`

Your Part 1 plants already compute `P_H * (1 + p_veg) * (1 + p_den)`. The
provided weather effects in `weather.py` multiply in the rest:

* **Slope**: `exp(a * slope_degrees)` with `a = 0.078`. Fire runs uphill,
  and row 0 (north) is uphill.
* **Wind**: `exp(V * (c1 + c2 * (cos(theta) - 1)))`, with wind speed `V`
  in m/s, `c1 = 0.045`, and `c2 = 0.131`. Fire races downwind. A fire
  creeping *into* the wind (a **backing fire**) is slow and gentle.
* **Fuel moisture**: `max(0, 1 - M / M_x)`, where `M` is the dead-fuel
  moisture and `M_x = 0.30` is the moisture of extinction. This follows the
  idea of Rothermel's (1972) moisture damping, simplified.

**Embers.** Spot fires 100-300 m ahead of a fire are common. An ember flies
3-10 squares downwind (farther in a stronger wind), and where it starts a
fire, that fire may throw another ember. Embers also start up to 90% of
home ignitions (IBHS), which is why Firewise home hardening matters.

**The burn day.** On the burn day, a holding crew patrols outside the burn
area and puts out most spot fires that land there. In calm air they catch
nearly all of them. The stronger the wind, the faster a spot fire grows,
and the more of them get away. The burn window is two weeks of daily
forecasts, and the burn happens on the first day that fits your
prescription. If no day fits, there is no burn this season. Burn-day winds
blow from the south, toward the north.

**Simplifications.** Real crews light strips one after another, starting
at the downwind line, so that each new strip burns into ground that has
already burned. Our crew lights the whole ignition line at once. Our
holding crew, burn window, and costs are teaching values, not measurements.

## Setup

Run the workspace's **Sync all workspace projects** task to pull Part 2 into
your `goodfire` folder. Part 2 only *adds* files; your Part 1 `cover.py`,
`sketch.py`, and `landscape.py` stay exactly as you left them. Then use
**Terminal → Run Task…** and pick a `Good Fire` task, or run from the
`goodfire` folder:

```sh
uv run python app3d.py                  # your chosen plan, historical climate
uv run python app3d.py --hotter-drier   # your chosen plan, hotter and drier
uv run python app3d.py --plan B         # watch plan B instead
uv run python app3d.py --no-plan        # the same season with no plan
uv run python compare_plans.py          # compare all five plans
uv run python -m pytest checks
```

The tasks **Good Fire: 3D Season, Choose a Plan...** and **Good Fire:
Compare One Plan...** ask which plan (A to E) to show.

3D controls: click the land to light a fire · Space pause · S one step ·
R restart · Up/Down speed · right-drag to orbit · scroll to zoom. Hover over
any square to see its `str()`.

## Files

| File | Yours? | What it holds |
| --- | --- | --- |
| `goodfire/cover.py`, `sketch.py`, `landscape.py` | from Part 1 | your Part 1 classes, unchanged |
| **`goodfire/burnplan.py`** | **yours** | five functions with sets and dictionaries; `fire_reach`, `control_line`, and `BurnPlan` are provided worked examples that use them |
| `goodfire/recursion.py` | provided | `spot_fire`: a worked example of recursion (an ember that starts a fire can throw another ember) |
| **`goodfire/plan.py`** | **yours** | `CHOSEN_PLAN`: the plan you choose |
| `goodfire/plans.py` | provided | the five season plans, A to E |
| `goodfire/fieldkit.py` | provided | turns the map into plain data (`land_map`, `neighbor_map`, `squares_of`) and other helpers |
| `goodfire/looks.py` | provided | gives every kind of square its `appearance()` for the 3D view |
| `goodfire/simulation.py` | provided | `Wildfire`: the burn day, then the season |
| `goodfire/weather.py`, `tactics.py` | provided | weather effects; fuel breaks, defensible space, water drops |
| `goodfire/part2_protocols.py`, `scenario.py` | provided | the protocols; the season's map, fires, budget, climates, and forecasts |
| `viewer3d.py`, `models3d.py`, `effects3d.py`, `app3d.py`, `compare_plans.py` | provided | the 3D sand table, and a side-by-side comparison of the plans |

The starter includes reference Part 1 files; your own Part 1 files work
too. As before, every file you hand in needs a module docstring,
`__author__`, and type annotations. Methods that already have code are
provided worked examples; each `raise NotImplementedError("TODO: ...")` is
yours.

## Your tasks

### Step 1: the burn plan (`burnplan.py`)

Write the five functions at the top of `burnplan.py`. Each one works only
on the values it is given, and none of them should change the lists, sets,
or dictionaries they are given. Test each one as you go: `uv run python -m pytest checks`
runs the provided checks.

**`count(kinds: list[str]) -> dict[str, int]`**: how many times each kind
of land appears in the list. Loop through the list; if a kind is already
a key, add 1 to its value, otherwise give it the value 1.

```python
count(["pine", "pine", "home"])  # returns {"pine": 2, "home": 1}
count([])  # returns {}
```

**`group_by_kind(land: dict[Square, str]) -> dict[str, set[Square]]`**:
the squares of each kind, as a set. Loop through the keys of `land`; the
first time you see a kind, give it an empty set (`set()`), then `add` the
square to that kind's set.

```python
a: Square = Square(0, 0)
b: Square = Square(0, 1)
c: Square = Square(1, 0)
land: dict[Square, str] = {a: "pine", b: "home", c: "pine"}
group_by_kind(land)  # returns {"pine": {a, c}, "home": {b}}
```

**`in_prescription(forecast: dict[str, float], prescription: dict[str,
list[float]]) -> bool`**: whether a day's forecast fits a prescription.
Each value in the prescription is a `[low, high]` range, and both ends are
allowed. Every condition the prescription names must be in the forecast
and inside its range. Conditions the prescription does not name do not
matter.

```python
rx: dict[str, list[float]] = {"wind": [1.0, 4.0], "moisture": [0.08, 0.2]}
in_prescription({"wind": 2.5, "moisture": 0.12}, rx)  # True
in_prescription({"wind": 4.0, "moisture": 0.08}, rx)  # True: ends count
in_prescription({"wind": 4.1, "moisture": 0.12}, rx)  # False: too windy
in_prescription({"wind": 2.5}, rx)  # False: no moisture
```

**`first_burn_day(forecasts: list[dict[str, float]], prescription: dict[str,
list[float]]) -> int`**: the index of the first forecast that fits the
prescription, or `-1` if none does. Use your `in_prescription`.

```python
calm: dict[str, list[float]] = {"wind": [1.0, 4.0]}
days: list[dict[str, float]] = [{"wind": 6.0}, {"wind": 2.0}, {"wind": 3.0}]
first_burn_day(days, calm)  # returns 1
first_burn_day([{"wind": 6.0}], calm)  # returns -1
```

The last function answers the question at the heart of a burn plan:
where can the fire go next?

**`spread_once(burning: set[Square], fuel: set[Square], neighbors:
dict[Square, list[Square]]) -> set[Square]`**: the squares fire spreads to
in one step. For each burning square, look at its neighbors
(`neighbors[square]`); a neighbor catches if it is fuel and is not
burning already. (The provided `control_line` at the bottom of the file
has almost the same shape: read it first.)

```python
# a - b - c   d    (a line of three squares, and d off on its own)
d: Square = Square(5, 5)
near: dict[Square, list[Square]] = {a: [b], b: [a, c], c: [b], d: []}
spread_once({a}, {a, b, c, d}, near)  # returns {b}
spread_once({a, b}, {a, b, c, d}, near)  # returns {c}
spread_once({a}, {a, c, d}, near)  # returns set(): b is not fuel
```

**Read `fire_reach`** (provided, right after `spread_once`). It uses your
`spread_once` to answer the bigger question: where could the fire reach
eventually? It starts with the start squares that are fuel, then calls
`spread_once` again and again, adding what catches, until a step catches
nothing new.

```python
fire_reach({a}, {a, b, c, d}, near)  # returns {a, b, c}: d is not connected
fire_reach({a}, {a, c, d}, near)  # returns {a}: b is not fuel
```

**See how the provided code uses them.** Read `control_line` and
`BurnPlan` at the bottom of `burnplan.py`. `BurnPlan.area()` groups the
whole map by kind (your `group_by_kind`), keeps the unit's squares of the
species to burn, takes away every home and every square next to a home,
and keeps what fire can reach from the ignition line (`fire_reach`, built
on your `spread_once`).
`control_line` finds every burnable square next to that area: fire can
leave only through those squares, so the crew mows a line there. The
simulation picks the burn day with your `first_burn_day`, and
`compare_plans.py` uses your `count` to report what burned off target.
Once all five work, the burn days in `compare_plans.py` and the 3D app
come to life.

### Step 2: choose a season plan (`plan.py`)

**Finish Step 1 first.** Plans A through D are built with your
`burnplan.py` functions. Until all five pass their checks
(`uv run python -m pytest checks`), those plans cannot run a burn day, so `compare_plans.py`
and the 3D app show them with no good fire and the comparison is
meaningless.

Your crew has five plans to choose from, in the provided `plans.py`. Each
one is a burn plan (built with your functions) plus tactics for the
wildfire season, all within one $40,000 budget:

| Plan | What it does |
| --- | --- |
| A | a small backing burn southeast of the road, and one fuel break |
| B | burn everything south of the river in strips on any day with wind up to 9 m/s, and Firewise the homes in the pines |
| C | burn everything south of the river in strips on a calm, damp day, with no Firewise work |
| D | burn everything south of the river in strips on a calm, damp day, and Firewise the homes in the pines |
| E | no burn: Firewise both neighborhoods and cut a fuel break |

Compare them:

```sh
uv run python compare_plans.py       # every plan over ten seasons, side by side
uv run python compare_plans.py B     # each season for plan B
uv run python app3d.py --plan B      # watch plan B in 3D
```

Then set `CHOSEN_PLAN` in `plan.py` to the letter of the plan that does
best on all three of these:

* **Habitat restored with good fire**: the more squares of pine and grass
  burned on burn days, the better.
* **The burn stays on target**: no home catches fire on a burn day, at
  most 30 squares burn off target, and the burn happens in at least 8 of
  the 10 seasons.
* **Homes kept safe** at the end of the season.

Before you choose, think about why each other plan falls short. What does
a backing fire alone accomplish? What happens to embers on a windy burn
day? Where do the homes in the pines sit, compared with the burn? And what
does a plan with no good fire give up?

Gradescope runs the plan you choose over the same 10 seasons
(5 seeds in both climates, 390 homes in all) and scores it:

| | Half credit | Full credit |
| --- | --- | --- |
| Habitat restored with good fire (squares) | 1,500 | 3,000 |
| The burn stays on target | | all three conditions above |
| Homes kept safe | 340 | 370 |

## Testing and submitting

Run **Terminal > Run Task... > Create EX06 - Good Fire Part 2 Submission** task and upload the ZIP
it writes into the `goodfire` folder to EX06 on Gradescope. It holds
`goodfire/burnplan.py` and `goodfire/plan.py`.

| Gradescope test | Points |
| --- | --- |
| Submission requirements (2 files x 1) | 2 |
| Functions and classes are where they belong | 5 |
| `count` | 13 |
| `group_by_kind` | 15 |
| `in_prescription` | 15 |
| `first_burn_day` | 12 |
| `spread_once` | 16 |
| `CHOSEN_PLAN` names one of the plans | 4 |
| Chosen plan: habitat restored | 7 |
| Chosen plan: the burn stays on target | 5 |
| Chosen plan: homes kept safe | 6 |
| **Total** | **100** |

## Sources

Alexandridis et al. (2008); Rothermel (1972), USDA Forest Service
INT-115; Wade and Lunsford (1989), *A Guide for Prescribed Fire in Southern
Forests*, USDA Forest Service Southern Region, R8-TP 11; FARSITE technical
documentation on spotting; IBHS (2019); NFPA Firewise USA; The Nature
Conservancy NC and the NC Forest Service on longleaf pine and prescribed
fire; Petrasova et al. (2018), *Tangible Modeling with Open Source GIS*;
EPA Climate Change Indicators: Wildfires; Climate Central (2024).
