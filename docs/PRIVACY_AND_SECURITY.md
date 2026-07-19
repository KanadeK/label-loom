# Privacy and security

Label Loom has no HTTP client, telemetry, analytics, account system, or cloud adapter. Input text, labels, outputs, and ledger files remain on the local filesystem chosen by the operator.

Treat source CSV files as potentially sensitive. Store them with appropriate filesystem access controls; review exports before sharing; avoid placing credentials, tokens, payment-card data, or customer identifiers in examples, issues, or commits. The built-in sample dataset is synthetic and may be used freely under the project MIT license.

The baseline is an assistive ranking tool. It may reflect errors or imbalance in supplied labels. A human reviewer remains responsible for final annotation and for assessing any downstream fairness, regulatory, or safety impact.
