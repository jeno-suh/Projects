from __future__ import annotations
from abc import ABC, abstractmethod

"""This module contains the necessary classes to implement the observer
design pattern.

Classes:
- Subject: Abstract base class for subjects
- Observer: Abstract base class for observers
"""

class Subject(ABC):
    """A simple interface for subjects from the observer pattern.

    Public Methods:
    - add_observer(observer: Observer) -> None
    - notify_observers() -> None
    """

    @abstractmethod
    def add_observer(self, observer: Observer) -> None:
        """Add an observer of the subject."""
        pass
    
    @abstractmethod
    def notify_observers(self) -> None:
        """Notify all observers about an event."""
        pass

class Observer(ABC):
    """A simple interface for observers from the observer pattern.

    Public Methods:
    - update(subject: Subject) -> None
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """Receive an update from subject."""
        pass