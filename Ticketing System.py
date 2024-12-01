from enum import Enum
from datetime import datetime
from typing import Dict, List, Optional, Tuple



class TicketState(Enum):
    CREATED = "CREATED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"
    DEAD = "DEAD"



class TicketPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"



class StateChange:
    def __init__(self, from_state, to_state, timestamp, comment):
        self.from_state = from_state
        self.to_state = to_state
        self.timestamp = timestamp
        self.comment = comment



class Ticket:
    def __init__(self, id, title, description, priority):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.current_state = TicketState.CREATED
        self.assigned_to = None
        self.history = []



class TicketingSystem:
    def __init__(self):
        self.tickets: Dict[str, Ticket] = {}
        self.transition_table = {
            TicketState.CREATED: {
                "assign": TicketState.ASSIGNED,
                "cancel": TicketState.CANCELLED,
                "invalidate": TicketState.DEAD
            },
            TicketState.ASSIGNED: {
                "start_work": TicketState.IN_PROGRESS,
                "invalidate": TicketState.DEAD
            },
            TicketState.IN_PROGRESS: {
                "hold": TicketState.ON_HOLD,
                "resolve": TicketState.RESOLVED,
                "cancel": TicketState.CANCELLED,
                "invalidate": TicketState.DEAD
            },
            TicketState.ON_HOLD: {
                "resume": TicketState.IN_PROGRESS,
                "cancel": TicketState.CANCELLED,
                "abandon": TicketState.DEAD
            },
            TicketState.RESOLVED: {
                "reopen": TicketState.IN_PROGRESS,
                "close": TicketState.CLOSED,
                "cancel": TicketState.CANCELLED,
                "finalize": TicketState.DEAD
            },
            TicketState.CANCELLED: {
                "finalize": TicketState.DEAD
            },
            TicketState.DEAD: {}
        }

    def create_ticket(self, ticket_id: str, title: str, description: str, priority: TicketPriority) -> Ticket:
        ticket = Ticket(id=ticket_id, title=title, description=description, priority=priority)
        self.tickets[ticket_id] = ticket
        return ticket

    def transition_ticket(self, ticket_id: str, action: str, comment: str = "", assigned_to: Optional[str] = None) -> Tuple[bool, str]:
        if ticket_id not in self.tickets:
            return False, "Ticket not found"

        ticket = self.tickets[ticket_id]
        current_state = ticket.current_state

        if current_state not in self.transition_table:
            return False, f"Invalid current state: {current_state}"

        if action not in self.transition_table[current_state]:
            return False, f"Invalid action '{action}' for state {current_state}"

        new_state = self.transition_table[current_state][action]
        
        
        state_change = StateChange(
            from_state=current_state,
            to_state=new_state,
            timestamp=datetime.now(),
            comment=comment
        )
        
        
        ticket.current_state = new_state
        ticket.history.append(state_change)
        if assigned_to is not None:
            ticket.assigned_to = assigned_to

        return True, f"Ticket transitioned from {current_state.value} to {new_state.value}"

    def get_ticket_history(self, ticket_id: str) -> List[StateChange]:
        if ticket_id not in self.tickets:
            return []
        return self.tickets[ticket_id].history



def main():
    
    system = TicketingSystem()

    
    ticket = system.create_ticket(
        "TICKET-001",
        "Login Issue",
        "User cannot login to the application",
        TicketPriority.HIGH
    )
    print(f"Created ticket: {ticket.id} - {ticket.title}")
    print(f"Initial state: {ticket.current_state.value}")

    
    while True:
        print("\nCurrent State:", ticket.current_state.value)
        
        # if current state is terminal
        if ticket.current_state not in system.transition_table or not system.transition_table[ticket.current_state]:
            print("This ticket is in a terminal state. No further actions are possible.")
            break

        print("Available actions:", list(system.transition_table[ticket.current_state].keys()))
        
        action = input("Enter an action (or 'exit' to quit): ").strip().lower()
        if action == "exit":
            break

        comment = input("Enter a comment for this action: ").strip()
        assigned_to = input("Enter assigned agent (leave blank if not applicable): ").strip() or None

        success, message = system.transition_ticket(ticket.id, action, comment, assigned_to)
        print(f"\nResult: {message}")
        if not success:
            print("Please try again with a valid action.")

    assign
    print("\nTicket History:")
    for change in system.get_ticket_history(ticket.id):
        print(f"{change.timestamp}: {change.from_state.value} → {change.to_state.value}")
        print(f"Comment: {change.comment}")


if __name__ == "__main__":
    main()
