# MixMidas Project Diagrams

## 1. Use-case diagram

```mermaid
flowchart LR
    Customer([Customer])
    Admin([Administrator])

    subgraph MixMidas
        Browse([Browse landing page])
        ViewServices([View services])
        Contact([Contact studio])
        Book([Book a session])
        Details([Enter booking details])
        Estimate([View estimated cost])
        Validate([Validate booking rules])
        Confirm([Receive booking confirmation])
        Login([Log in])
        Manage([View and manage bookings])
    end

    Customer --> Browse
    Customer --> ViewServices
    Customer --> Contact
    Customer --> Book
    Book --> Details
    Book --> Estimate
    Book --> Validate
    Book --> Confirm
    Admin --> Login
    Admin --> Manage
    Login --> Manage
```

**Description:** Customers can explore the site, contact MixMidas, and make a booking. A booking requires customer details, service, date, start time, and duration. The system calculates the cost at ₦10,000 per hour and validates that the session is within 10 AM–6 PM, is not in the past, and does not overlap another session. An administrator logs into Django administration to view and manage stored bookings.

## 2. Sequence diagram

```mermaid
sequenceDiagram
    actor Customer
    participant Browser
    participant Django as Django view
    participant Form as BookingForm
    participant DB as PostgreSQL database

    Customer->>Browser: Open booking page
    Browser->>Django: GET /book/
    Django-->>Browser: Render booking form
    Customer->>Browser: Submit booking details
    Browser->>Django: POST /book/
    Django->>Form: Validate submitted data
    Form->>DB: Check existing sessions on selected date
    DB-->>Form: Return matching bookings
    alt Booking is valid
        Form-->>Django: Valid booking data
        Django->>DB: Save Booking record
        DB-->>Django: Confirm record saved
        Django-->>Browser: Render confirmation popup
        Browser-->>Customer: Show service, date, duration and total
    else Booking is invalid
        Form-->>Django: Return validation errors
        Django-->>Browser: Re-render form with errors
        Browser-->>Customer: Show correction message
    end
```

**Description:** The customer opens the booking page and submits the form. Django passes the submitted details to `BookingForm`, which applies the service-hour and scheduling rules and queries the database for time conflicts. A valid booking is stored and the customer sees a confirmation modal. Invalid input returns to the same form with an explanation.

## 3. Class diagram

```mermaid
classDiagram
    class Booking {
        +String name
        +Email email
        +Service service
        +Date date
        +Time start_time
        +Integer duration_hours
        +Text project_details
        +DateTime created_at
        +Integer total_cost
    }

    class BookingForm {
        +clean_start_time()
        +clean()
        +label_for_hour(hour)
    }

    class BookingAdmin {
        +list_display
        +list_filter
        +search_fields
        +ordering
    }

    class Views {
        +home(request)
        +book_session(request)
    }

    class User {
        +username
        +email
        +password
        +is_staff
        +is_superuser
    }

    BookingForm --> Booking : creates and validates
    Views --> BookingForm : processes
    Views --> Booking : saves and displays
    BookingAdmin --> Booking : administers
    User --> BookingAdmin : authenticated access
```

**Description:** `Booking` is the central database model and stores every customer session. `BookingForm` creates the booking form and contains the scheduling validation rules. The view functions display the landing page, process booking submissions, and show confirmation details. `BookingAdmin` exposes booking records in Django administration. Django’s `User` model controls administrator authentication and access to the booking records.
