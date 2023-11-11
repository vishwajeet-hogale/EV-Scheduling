# EV-Scheduling
Greedy approach to assign EVs to EV charging stations
## Project Overview: Electric Vehicle Charging Allocation

This repository addresses the Electric Vehicle (EV) charging allocation problem by providing both offline and online solutions. In this project, EV users are treated as self-interested agents seeking to maximize profit while minimizing schedule impact.

### Key Features:
- Use of djkstra's algorithm to schedule EVs and pricing mechanisms for EV stations.
- Formulation of the optimal EV-to-charging station allocation as a Mixed Integer Programming (MIP) problem.
- Development of a solution that incrementally utilizes the MIP-based greedy algorithm to efficiently handle EV charging stations and pricing.
- Takes distance to station, fuel capacity, time, average EV speed, availability of stations, time taken to charge in consideration while scheduling EVs at their respective stations


### Online Algorithm Efficiency:
- The algorithm is capable of handling and scheuling more than 1000 EVs with 91% efficiency.

## How to Use:
1. Clone the repository.
2. Add the meta data related to the EVs in all_details.py file
3. Execute djkstra.py


### Contributing:
Contributions and feedback are welcome. Please follow the guidelines outlined in `CONTRIBUTING.md`.

### License:
This project is licensed under the [MIT License](LICENSE).

Feel free to explore the codebase and contribute to the advancement of Electric Vehicle charging allocation solutions!
