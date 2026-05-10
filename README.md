# Nordic Finance & Credit Developer

The goal is not just to write code, but to **understand the business domain**, regulations, and apply software engineering standards for the European/Nordic financial sector. We will build independent sub-projects step-by-step.

---

## 🗺️ Roadmap (Study and Development Plan)

### Sub-project 1: Loan Lifecycle Engine (`01_Loan_Lifecycle_Engine`)
**Objective:** Master the foundations of financial mathematics, a critical requirement for translating financial models into efficient code.
*   **Amortization Models:** We will build from scratch the algorithms for:
    *   **French System** (Constant Payment - *Annuitetslån*).
    *   **German System** (Constant Principal Repayment, Decreasing Payment - *Serielån*).
    *   **American System** (Interest Only, Bullet Payment).
*   **Rate Management:** Calculation of nominal vs. effective interest rates and equivalent rates.
*   **Financial Precision:** Generation of amortization schedules accurate to the cent using proper decimal handling (vital for avoiding rounding errors in audits).
*   **Language:** Python.

### Sub-project 2: Nordic Risk & Compliance Engine (`02_Nordic_Compliance_Scoring`)
**Objective:** Implement credit assessment and risk management logic based on real market regulations.
*   Credit scoring models.
*   Evaluation factors for mortgage products according to regulations like *Finanstilsynet* (Norway/Denmark).
*   Examples of financial stress testing (e.g., LTI, LTV, interest rate hike tolerance).

### Sub-project 3: Persistence and Integration Architecture (`03_Data_Integration_API`)
**Objective:** Manage complex data models and system communication.
*   Structured relational design to historize transactions, early payments, and audits.
*   REST API development to expose the calculation engines.
*   Domain-Driven Design (DDD) practices.

### Sub-project 4: Enterprise Migration (Java / C#) (`04_Enterprise_Migration`)
**Objective:** Adapt what we learned to the environment and language of an Enterprise core banking architecture.
*   Translation of the Python core calculation engine to Java or C#.
*   High availability design, concurrency, and deployment (Docker/Cloud).

---

> **Note:** Each sub-project will have its own structure and dependencies. There will be a strong focus on Clean Code, exhaustive Testing (Unit & Regression Tests), and the use of AI assistants to accelerate development.
