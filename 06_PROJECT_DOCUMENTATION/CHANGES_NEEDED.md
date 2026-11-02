# Verified Facts for Review-II Documentation Fixes

## 1. Codebase Truths (Resolving Inconsistencies a-f)
a. **Training Attack Prevalence:** 6.10% (21,344 attacks out of 350,000 flows). The report's claim of 0.35% is incorrect (it mistakenly quotes the validation prevalence).
b. **Historical-Error Risk Signal:** Sourced from **training set errors** (predictions vs y_train), mapping error rates over deciles to 10 features.
c. **Mahalanobis (OOD) Configuration:** Computes the pseudo-inverse (
p.linalg.pinv) with a small regularization (eps=1e-6) on a random sample of 50,000 training points. The report's claim of lambda=1e-4 on 350K points is outdated/incorrect.
d. **Static Multi-Factor Strategy:** Implemented as a 2-signal blend (50% confidence risk, 50% OOD risk). The 4-signal blend is called "Four-Factor Strategy".
e. **Uncertainty Range:** Mapped to [0, 0.5], derived from 1 - confidence, where confidence for a binary classifier spans [0.5, 1.0].
f. **Label Leakage in Adaptive Loop:** **None.** Test labels (y_shifted_test.csv) are strictly read *after* review scores have queued predictions. No test labels influence the adaptive weighting.

## 2. Implementation Progress (FR1 - FR14)
- **FR1 to FR13:** 100% Implemented. Supported by Python scripts in src/.
- **FR14 (Dashboard):** 50% (Partially Implemented). Exists locally for Phase-I.
- **Progress Calculation:** (13 * 100% + 1 * 50%) / 14 = **96.4%**.

## 3. Other TODOs
- Add AI-use disclosure to README.md and Capstone Report.
- Use exact DOI/Scopus references.
