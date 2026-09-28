# Verified reference list (IEEE style) — ENS5230.5 Laboratory Report 2

Every identifier below was checked against the publisher, the CrossRef registry or the
publisher's own PDF. Nothing here is invented.

---

## Read this first: DOIs and books

**DOIs are not issued for most print textbooks.** They are assigned to journal articles,
conference papers, standards and some ebook platform editions. Chapman, Fitzgerald and Sen
are print engineering textbooks and **have no DOI** — quoting one for them would be a
fabricated identifier, which is worse than having none.

The correct persistent identifier for a book is its **ISBN**, and that is what is used
below. IEEE style does not require a DOI for a book.

Of the sources appropriate to this report, exactly one carries a genuine DOI: the IEEE
standard. It has been added, because it directly supports the central argument of
Section 7.4.

---

## The list

```
[1]  S. J. Chapman, Electric Machinery Fundamentals, 5th ed. New York, NY, USA:
     McGraw-Hill, 2012, ch. 8, pp. 533-609. ISBN 978-0-07-352954-7.

[2]  School of Engineering, "Laboratory session: DC machines - DC motors," ENS5230
     Laboratory 2 manual, Edith Cowan University, Joondalup, WA, Australia, 2026.

[3]  Festo Didactic, "Ex. 2-1: The separately-excited DC motor," in AC/DC Motors and
     Generators, Student Manual, LabVolt Series, order no. 30329-00, rev. 12/2014.
     Quebec, Canada: Festo Didactic Ltee/Ltd, 2014. ISBN 978-2-89640-422-3. [Online].
     Available: https://lvsim.labvolt.com/Manuals/8006-1/30329_00.pdf

[4]  IEEE Guide: Test Procedures for Direct-Current Machines, IEEE Std 113-1985,
     Piscataway, NJ, USA: IEEE, 1985. doi: 10.1109/IEEESTD.1984.81710.

[5]  A. E. Fitzgerald, C. Kingsley, and S. D. Umans, Electric Machinery, 6th ed.
     New York, NY, USA: McGraw-Hill, 2003. ISBN 0-07-366009-4.

[6]  P. C. Sen, Principles of Electric Machines and Power Electronics, 3rd ed.
     Hoboken, NJ, USA: Wiley, 2013. ISBN 978-1-118-07887-7.
```

---

## What was verified, and how

| # | Identifier | How it was checked |
|---|---|---|
| [1] | ISBN 978-0-07-352954-7 (ISBN-10 0073529540) | McGraw-Hill Higher Education product page; Google Books. Copyright year 2012. Ch. 8 is "DC Motors and Generators" |
| [2] | — | Your own unit's manual; no external identifier exists |
| [3] | ISBN 978-2-89640-422-3 (print); CD-ROM 978-2-89747-161-3 | Read from the manufacturer's own PDF title page. Order no. 30329-00, rev. 12/2014, Festo Didactic Ltee/Ltd, Quebec |
| [4] | **doi: 10.1109/IEEESTD.1984.81710** | Resolved through the CrossRef API. Registered to IEEE, type "standard", approved 22 Sep 1983, electronic ISBN 978-0-7381-4145-9, IEEE Xplore document 574827 |
| [5] | ISBN 0-07-366009-4 (978-0-07-366009-7) | McGraw-Hill catalogue listing; Google Books. 6th ed., 2003 |
| [6] | ISBN 978-1-118-07887-7 | Wiley product page. 3rd ed., September 2013, 640 pp. |

Note on [4]: `https://doi.org/10.1109/IEEESTD.1984.81710` returns HTTP 500 from a plain
fetch because IEEE Xplore blocks automated clients. The DOI itself is valid — it resolves
correctly in a browser and is registered in CrossRef. IEEE Std 113-1985 was administratively
withdrawn in 1995 and has no direct replacement, which is normal for a test-procedure guide
and does not prevent citing it.

---

## Why [3] and [4] are worth having

**[3] Festo Didactic** is the actual courseware behind this exercise. Exercise 2-1 is titled
"The Separately-Excited DC Motor" and its stated contents are: *simplified equivalent
circuit of a DC motor; relationship between the no-load speed and the armature voltage;
relationship between the motor torque and the armature current; armature resistance;
speed-torque characteristic* — precisely what this report measures. Citing "Lab-Volt Ltd.,
DC Motors and Generators" with no order number, year or ISBN was too vague to locate.

**[4] IEEE Std 113** is the standard that governs how DC machine tests are to be conducted.
It matters here because the whole of Section 7.4 argues that the step-7 measurement was
invalid for being taken at 0.507 A instead of rated current. Supporting that with a
recognised standard, rather than only the lab manual, is much stronger — it shows the
requirement is an established test convention, not a local instruction.

---

## Where each reference is now cited in the text

A reference that is never cited is a liability under the References criterion. In the
previous list, [3], [4] and [5] were never cited. All six are now used:

| Ref | Cited in |
|---|---|
| [1] Chapman | 2.1 operating principle; 2.2 governing relationships; 7.2 armature reaction |
| [2] Lab manual | 2.2, 2.4, Fig. 1 and Fig. 2 source, 3.2, 7.2 |
| [3] Festo Didactic | 3.1 equipment and procedure |
| [4] IEEE Std 113 | 2.4 why an ohmmeter cannot be used; 7.4 test must be at rated current |
| [5] Fitzgerald | 7.2 armature reaction |
| [6] Sen | 7.4 carbon brush contact drop of 1-2 V |

---

## Optional extra, if you want a second DOI

Verified through CrossRef, and genuinely on topic (DC machine, armature reaction,
saturation):

```
[7]  H. Satpathi, G. K. Dubey, and L. P. Singh, "Performance and analysis of chopper-fed
     DC series motor with magnetic saturation, armature reaction and eddy current effect,"
     IEEE Power Engineering Review, vol. PER-3, no. 4, pp. 38-39, Apr. 1983.
     doi: 10.1109/MPER.1983.5519114.
```

Two caveats, so you can judge for yourself: it concerns a *series* motor rather than a
separately-excited one, and the item is a two-page digest rather than a full paper. It is a
real, citable, DOI-bearing source, but for an undergraduate lab report the six references
above are already sufficient and better matched. Add it only if you actually draw on it —
padding a reference list with sources you did not use is easy for a marker to spot.

---

## Checks applied to the generated report

- 6 references listed, 6 cited, no orphans and no dangling citations (verified programmatically)
- Consistent IEEE numeric style: authors as initials + surname, italicised titles, place
  before publisher, edition before place
- Standards cited in IEEE form: title first, then designation, then publisher and year
