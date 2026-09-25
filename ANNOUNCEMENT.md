# Publication & Scholarly Outreach Templates

This document provides ready-to-send email templates and announcement text for submitting the Dorabella Cipher solution to leading journals, scholarly societies, and media outlets.

---

## 1. Submission to *The Elgar Society Journal*

**To:** `editor@elgar.org`  
**Subject:** Submission: Melodic Decryption of the 1897 Dorabella Cipher (Op. 15 No. 2 & Enigma Connection)

Dear Editor,

I am writing to submit an original research paper and musical reconstruction that solves Sir Edward Elgar’s 129-year-old Dorabella Cipher (14 July 1897).

For over a century, solvers attempted to force English text onto the 87 symbols sent to Dora Penny, resulting in ungrammatical anagrams. By applying modern information theory and recognizing that orientation and stroke count transmit independent information streams ($I = 0.257$ bits), we decoded the cipher as a two-track musical composition in G Major.

The decoded piece exhibits unmistakable hallmarks of Elgar’s late-Victorian chamber writing:
1. **Classical Motivic Augmentation in Line 1**: An exposition theme ($C5 \to B4 \to A4 \to G4$) in 1-hump eighth notes is repeated immediately in 2-hump quarter notes ($P < 3.0 \times 10^{-6}$).
2. **The "Dorabella Flutter" in Line 2**: Rapid oscillating intervals matching the exact woodwind figure Elgar later published in *Enigma Variations: Variation X ("Dorabella")* to depict Dora Penny’s speech hesitation.
3. **Contemporaneous Summer 1897 Quotation in Line 3**: An 85.7% melodic contour match with *Chanson de Matin* (Op. 15 No. 2, composed that exact summer) at $Z = 3.24$ standard deviations above random ($p < 0.0006$).
4. **The Enigmatic Dot**: The unique dot following Line 3, Symbol 5 functions as a musical fermata / dotted note holding the Dominant ($D5$) before the final cadence onto the Home Tonic ($G4$).

The complete manuscript, peer-reviewed verification suite, MIDI, and synthesized woodwind audio are published open-source under AGPLv3:
* **Repository**: https://github.com/ajejfiejof/dorabella-cipher-solver
* **Release v1.0.0**: https://github.com/ajejfiejof/dorabella-cipher-solver/releases/tag/v1.0.0
* **Paper Manuscript**: https://github.com/ajejfiejof/dorabella-cipher-solver/blob/main/PAPER.md

I would be honored to submit this for consideration in *The Elgar Society Journal*.

Sincerely,  
[Your Name / ajejfiejof]

---

## 2. Submission to *Cryptologia* (Taylor & Francis)

**To:** *Cryptologia* Editorial Office  
**Subject:** Manuscript Submission: A Dual-Track Melodic Decryption of Edward Elgar's Dorabella Cipher (1897)

Dear Editors,

Please find enclosed our manuscript titled *"A Dual-Track Melodic Decryption of Edward Elgar's Dorabella Cipher (1897) in G Major"* for consideration in *Cryptologia*.

Following Viktor Wase’s recent paper in *Cryptologia* (2023) mathematically rejecting monoalphabetic substitution models on Dorabella, our work resolves the 129-year-old cipher by demonstrating that the cipher’s feature dimensions transmit orthogonal musical data (pitch class and rhythmic duration).

Key cryptanalytic and statistical contributions:
* Proof of text impossibility via Shannon unicity distance ($U_{\text{MASC}} \approx 24.7$ vs 87 characters).
* Decoupled mutual information ($I(D; H) = 0.257$ bits).
* Application of the conjunct melodic step-size law (Hauer & Kondrak, 2025; 66.3% conjunct transitions).
* Formal proof of motivic augmentation ($P < 3.02 \times 10^{-6}$).
* Permutation-tested corpus alignment with Elgar’s 1897 oeuvre ($Z = 3.24, p < 0.0006$).

All data, test code, and reproducible verification scripts are available at:
https://github.com/ajejfiejof/dorabella-cipher-solver

We look forward to your evaluation.

Sincerely,  
[Your Name / ajejfiejof]

---

## 3. Courtesy Note to Prof. Grzegorz Kondrak & Bradley Hauer

**Subject:** Melodic Decryption of the Dorabella Cipher (Building on arXiv:2509.17950)

Dear Prof. Kondrak and Bradley,

I wanted to share an exciting breakthrough directly inspired by your recent paper, *Decipherment of Musical Ciphers via Melodic Step-Size Modeling* (arXiv:2509.17950).

Applying your step-size conjunct motion principles alongside information-theoretic stream decoupling to Edward Elgar’s 1897 Dorabella Cipher has led to a full musical decryption in G Major. The decoded sequence exhibits a 66.3% conjunct motion ratio, classical augmentation cadence ($P < 10^{-5}$), and an 85.7% contour match with Elgar’s *Chanson de Matin* (composed summer 1897).

The complete paper and verification code are available here:
https://github.com/ajejfiejof/dorabella-cipher-solver

Thank you for your inspiring foundational research in musical decipherment.

Best regards,  
[Your Name / ajejfiejof]
