from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self

# Note:
# 'Task' to define what to do
# Group of tasks as a 'python list'?
# Collection of groups? 

@dataclass
class Task:
    name: str
    done: bool
    priority: int
    description: Optional[str]
    created: datetime
    due: Optional[datetime]
    finished: Optional[datetime]

    @staticmethod
    def new(
        name: str,
        priority: Optional[int] = None,
        description: Optional[str] = None,
        due: Optional[datetime] = None,
    ) -> Self:
        priority = priority if priority else 10
        description = description if description else ""

        return Task(
            name=name,
            done=False,
            priority=priority,
            description=description,
            created=datetime.now(),
            finished=None,
            due=due,
        )
    
    def set_done(self) -> None:
        # TODO: Not the best of names.
        if not self.done:
            self.done = True
            self.finished = datetime.now()

