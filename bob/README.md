# Bob

Swarm Agent for a user called bob.

# Setup for the the `bob` agent

```bash
swarm_manager ~/.swarm_test --new_agent bob
swarm_manager ~/.swarm_test --register_agent_id bob # requires an existing `did_chain` agent
swarm_manager ~/.swarm_test --set_broker bob broker # requires an existing `broker` agent
```

# Run the agent

```bash
SWARM_BASE_DIR=~/.swarm_test python examples/bob/main.py
```
