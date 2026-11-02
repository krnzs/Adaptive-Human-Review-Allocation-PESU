# FR14 Status & Phase-II Roadmap

**Project:** Adaptive Human-Review Allocation for Reliable Machine Learning Under Distribution Shift  
**Student:** Karan Shetty (`PES1PG25CA101`) | **Faculty Guide:** Dilip Kumar Maripuri  
**Institution:** PES University, Department of Computer Applications  
**Official Status Statement:** **“13 of 14 functional requirements are fully implemented; FR14 is partially implemented (92.9% fully implemented).”**  

---

## 1. Specification of Functional Requirement 14

### Requirement Title
**FR14: Multi-Dataset Web Portal & Cross-Domain Deployment**

### Original Specification Scope
> *"The system shall provide an interactive graphical web interface to visualize review allocations, and support ingestion of diverse datasets across multiple domains (e.g., cybersecurity, financial fraud, medical diagnosis) with cloud-native multi-tenant deployment."*

---

## 2. What Is Currently Implemented (Why FR14 is Partial)

1. **Interactive Operational Dashboard (`dashboard/app.py`):**
   - Full Streamlit-based web dashboard designed specifically for the NF-UQ-NIDS-v2 benchmark dataset (500,000 flows).
   - Interactive review capacity slider ($1\%, 2\%, 5\%, 10\%$).
   - Multiselect strategy filter comparing all five review strategies.
   - Dynamic yield curves (errors caught per 1,000 reviews).
   - PSI distribution drift ranking highlighting shifted features (`L4_SRC_PORT`, `IN_BYTES`).
   - Four reliability signals diagnostic cards with explicit mathematical ranges.
   - Sequential 5-batch online adaptation trace showing $w_{\text{hist}}$ progression ($0.25 \rightarrow 0.40$).
   - Direct CSV data export via `st.download_button`.
   - Explicit zero-leakage and offline simulation methodology notices.

---

## 3. What Remains Incomplete & Why It Is Deferred to Phase-II

| Component | Status | Technical Reason for Deferral |
| :--- | :---: | :--- |
| **Universal Multi-Dataset Ingestion** | Deferred | Requires dynamic schema inference and automated feature mapping for non-NetFlow tabular data (e.g., credit card fraud, medical records). |
| **Cross-Domain Evaluation** | Deferred | In Phase-I, all research was rigorously focused on establishing the ground-truth benchmark on NF-UQ-NIDS-v2 (500K flows). Cross-domain validation is a dedicated Phase-II research goal. |
| **Enterprise Cloud Multi-Tenancy** | Deferred | Cloud deployment (AWS ECS / Kubernetes / OAuth authentication) requires external cloud infrastructure and recurring hosting costs that fall outside the academic scope of an individual MCA capstone. |

---

## 4. Minimum Steps to Complete FR14 in Phase-II

1. **Step 1 (Schema-Agnostic Ingestion Engine):**
   - Implement an automated feature classification module that inspects uploaded CSVs, identifies numeric and categorical columns, and flags timestamp columns for chronological splitting.
2. **Step 2 (Cross-Domain Datasets):**
   - Ingest IEEE-CIS Fraud Detection dataset and MIMIC-III clinical records to evaluate the 4 reliability signals across non-network domains.
3. **Step 3 (Containerization & Cloud Deployment):**
   - Create a `Dockerfile` and `docker-compose.yml` configuration.
   - Deploy as a containerized microservice on AWS Elastic Container Service (ECS) with role-based access control.

---

## 5. Viva Demonstration Script for FR14

When asked by examiners about FR14:
> *"FR14 specified a web interface and multi-domain deployment. We have fully implemented the operational dashboard in Streamlit for our primary benchmark dataset, NF-UQ-NIDS-v2. It provides real-time exploration of budgets, strategy comparisons, drift rankings, and sequential feedback traces. As formally recorded in our project milestones, enterprise cloud multi-tenancy and cross-domain financial/medical datasets are designated as Phase-II future work, which is why our project is at 92.9% completion (13 of 14 functional requirements fully implemented)."*
