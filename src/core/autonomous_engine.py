import asyncio

class AutonomousEngine:
    def __init__(self, planner, executor, critic, memory):
        self.planner = planner
        self.executor = executor
        self.critic = critic
        self.memory = memory

    async def run_goal(self, goal: str, providers):
        plan = await self.planner.create_plan(goal, self.memory)

        results = []

        for step in plan["steps"]:
            result = await self.executor.execute(step, providers)
            results.append(result)

            review = await self.critic.review(step, result)

            if not review["pass"]:
                correction = review["fix"]
                result = await self.executor.execute(correction, providers)
                results.append(result)

        self.memory.store(goal, results)

        return {
            "goal": goal,
            "plan": plan,
            "results": results
        }
