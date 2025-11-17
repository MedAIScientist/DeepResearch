# Citation Styles Guide

This document provides comprehensive examples and guidelines for the citation styles supported by Gazzali Research. The system supports four major academic citation styles: APA, MLA, Chicago, and IEEE.

## Table of Contents

- [Overview](#overview)
- [APA Style (7th Edition)](#apa-style-7th-edition)
- [MLA Style (9th Edition)](#mla-style-9th-edition)
- [Chicago Style (17th Edition)](#chicago-style-17th-edition)
- [IEEE Style](#ieee-style)
- [Inline Citations](#inline-citations)
- [Bibliography Formatting](#bibliography-formatting)
- [Special Cases](#special-cases)
- [Usage in Gazzali Research](#usage-in-gazzali-research)

## Overview

Gazzali Research automatically tracks and formats citations in multiple academic styles. The citation manager:

- Captures bibliographic metadata from all sources
- Formats citations according to style guidelines
- Generates properly formatted bibliographies
- Handles inline citations in text
- Exports to BibTeX and RIS formats

### Supported Styles

| Style | Full Name | Common Disciplines | Inline Format |
|-------|-----------|-------------------|---------------|
| APA | American Psychological Association (7th ed.) | Psychology, Education, Social Sciences | (Author, Year) |
| MLA | Modern Language Association (9th ed.) | Literature, Humanities, Arts | (Author Page) |
| Chicago | Chicago Manual of Style (17th ed.) | History, Arts, Humanities | (Author Year) |
| IEEE | Institute of Electrical and Electronics Engineers | Engineering, Computer Science, Technology | [Number] |

## APA Style (7th Edition)

APA style is widely used in psychology, education, and social sciences. It emphasizes the date of publication and uses an author-date citation system.

### Key Features

- Author-date inline citations: (Smith, 2020)
- Hanging indent for bibliography entries
- Sentence case for article titles
- Title case for journal names
- DOI or URL at the end

### Journal Article Examples

**Single Author:**
```
Smith, J. A. (2020). The impact of artificial intelligence on cognitive development. 
    Journal of Cognitive Psychology, 45(3), 234-256. https://doi.org/10.1234/jcp.2020.45.3.234
```

**Two Authors:**
```
Johnson, M. R., & Williams, K. L. (2019). Machine learning approaches to natural 
    language processing. Computational Linguistics, 38(2), 145-178. 
    https://doi.org/10.1234/cl.2019.38.2.145
```

**Three or More Authors:**
```
Chen, L., Rodriguez, A. M., & Patel, S. K. (2021). Deep learning architectures for 
    image recognition. Computer Vision Research, 52(4), 567-589. 
    https://doi.org/10.1234/cvr.2021.52.4.567
```

**More Than 20 Authors:**
```
Anderson, B. C., Brown, D. E., Clark, F. G., Davis, H. I., Evans, J. K., Foster, L. M., 
    Green, N. O., Harris, P. Q., Irving, R. S., Jackson, T. U., King, V. W., Lewis, X. Y., 
    Martin, Z. A., Nelson, B. C., Oliver, D. E., Parker, F. G., Quinn, H. I., Roberts, J. K., 
    Stevens, L. M., ... Zhang, Y. Z. (2022). Large-scale collaborative research in 
    neuroscience. Nature Neuroscience, 25(6), 789-812. 
    https://doi.org/10.1234/nn.2022.25.6.789
```

### Conference Paper Examples

**Conference Proceedings:**
```
Kumar, R., & Lee, S. (2020). Blockchain applications in healthcare systems. In 
    Proceedings of the International Conference on Healthcare Technology (pp. 123-135). 
    https://doi.org/10.1234/icht.2020.123
```

### Book Examples

**Entire Book:**
```
Thompson, R. A. (2018). Cognitive development in early childhood. Academic Press.
```

**Edited Book:**
```
Martinez, C. D., & Wilson, E. F. (Eds.). (2019). Advances in machine learning. 
    MIT Press.
```

### Web Sources

**Web Page:**
```
National Institute of Health. (2021). Guidelines for ethical research practices. 
    https://www.nih.gov/research-ethics
```

**No Author:**
```
[No author]. (2020). Climate change impacts on biodiversity. Environmental Science 
    Portal. https://www.envscience.org/climate-biodiversity
```

### Inline Citation Examples

**Basic Citation:**
- Single author: `(Smith, 2020)`
- Two authors: `(Johnson & Williams, 2019)`
- Three or more: `(Chen et al., 2021)`

**With Page Numbers:**
- `(Smith, 2020, p. 45)`
- `(Johnson & Williams, 2019, pp. 23-25)`

**Multiple Citations:**
- `(Chen et al., 2021; Smith, 2020; Williams, 2019)`

**No Date:**
- `(Smith, n.d.)`

## MLA Style (9th Edition)

MLA style is commonly used in literature, humanities, and arts. It emphasizes the author and uses a simplified citation format.

### Key Features

- Author-page inline citations: (Smith 45)
- Works Cited list (not References)
- Title case for all titles
- Hanging indent for bibliography entries
- Access dates for web sources

### Journal Article Examples

**Single Author:**
```
Smith, John A. "The Impact of Artificial Intelligence on Cognitive Development." 
    Journal of Cognitive Psychology, vol. 45, no. 3, 2020, pp. 234-256. 
    https://doi.org/10.1234/jcp.2020.45.3.234.
```

**Two Authors:**
```
Johnson, Mary R., and Karen L. Williams. "Machine Learning Approaches to Natural 
    Language Processing." Computational Linguistics, vol. 38, no. 2, 2019, pp. 145-178. 
    https://doi.org/10.1234/cl.2019.38.2.145.
```

**Three or More Authors:**
```
Chen, Li, et al. "Deep Learning Architectures for Image Recognition." Computer Vision 
    Research, vol. 52, no. 4, 2021, pp. 567-589. 
    https://doi.org/10.1234/cvr.2021.52.4.567.
```

### Conference Paper Examples

```
Kumar, Raj, and Sarah Lee. "Blockchain Applications in Healthcare Systems." 
    Proceedings of the International Conference on Healthcare Technology, 2020, 
    pp. 123-135. https://doi.org/10.1234/icht.2020.123.
```

### Book Examples

**Entire Book:**
```
Thompson, Robert A. Cognitive Development in Early Childhood. Academic Press, 2018.
```

**Edited Book:**
```
Martinez, Carlos D., and Emily F. Wilson, editors. Advances in Machine Learning. 
    MIT Press, 2019.
```

### Web Sources

**Web Page:**
```
National Institute of Health. "Guidelines for Ethical Research Practices." 2021. 
    https://www.nih.gov/research-ethics. Accessed 15 Nov. 2024.
```

**No Author:**
```
"Climate Change Impacts on Biodiversity." Environmental Science Portal, 2020. 
    https://www.envscience.org/climate-biodiversity. Accessed 15 Nov. 2024.
```

### Inline Citation Examples

**Basic Citation:**
- Single author: `(Smith 45)`
- Two authors: `(Johnson and Williams 23)`
- Three or more: `(Chen et al. 567)`

**No Page Number:**
- `(Smith)`

**Multiple Citations:**
- `(Chen et al. 567; Smith 45; Williams 12)`

## Chicago Style (17th Edition)

Chicago style offers two systems: notes-bibliography (common in humanities) and author-date (common in sciences). Gazzali Research implements the author-date system.

### Key Features

- Author-date inline citations: (Smith 2020)
- Comprehensive bibliography entries
- Title case for titles
- Flexible formatting options
- Full publication details

### Journal Article Examples

**Single Author:**
```
Smith, John A. 2020. "The Impact of Artificial Intelligence on Cognitive Development." 
    Journal of Cognitive Psychology 45, no. 3: 234-256. 
    https://doi.org/10.1234/jcp.2020.45.3.234.
```

**Two Authors:**
```
Johnson, Mary R., and Karen L. Williams. 2019. "Machine Learning Approaches to Natural 
    Language Processing." Computational Linguistics 38, no. 2: 145-178. 
    https://doi.org/10.1234/cl.2019.38.2.145.
```

**Three Authors:**
```
Chen, Li, Ana M. Rodriguez, and Sanjay K. Patel. 2021. "Deep Learning Architectures 
    for Image Recognition." Computer Vision Research 52, no. 4: 567-589. 
    https://doi.org/10.1234/cvr.2021.52.4.567.
```

**Four or More Authors:**
```
Anderson, Brian C. et al. 2022. "Large-Scale Collaborative Research in Neuroscience." 
    Nature Neuroscience 25, no. 6: 789-812. https://doi.org/10.1234/nn.2022.25.6.789.
```

### Conference Paper Examples

```
Kumar, Raj, and Sarah Lee. 2020. "Blockchain Applications in Healthcare Systems." 
    In Proceedings of the International Conference on Healthcare Technology, 123-135. 
    https://doi.org/10.1234/icht.2020.123.
```

### Book Examples

**Entire Book:**
```
Thompson, Robert A. 2018. Cognitive Development in Early Childhood. Academic Press.
```

**Edited Book:**
```
Martinez, Carlos D., and Emily F. Wilson, eds. 2019. Advances in Machine Learning. 
    MIT Press.
```

### Web Sources

```
National Institute of Health. 2021. "Guidelines for Ethical Research Practices." 
    https://www.nih.gov/research-ethics.
```

### Inline Citation Examples

**Basic Citation:**
- Single author: `(Smith 2020)`
- Two authors: `(Johnson and Williams 2019)`
- Three or more: `(Chen et al. 2021)`

**With Page Numbers:**
- `(Smith 2020, 45)`
- `(Johnson and Williams 2019, 23-25)`

**Multiple Citations:**
- `(Chen et al. 2021; Smith 2020; Williams 2019)`

## IEEE Style

IEEE style is used in engineering, computer science, and technology fields. It uses a numbered citation system.

### Key Features

- Numbered inline citations: [1]
- References numbered in order of appearance
- Abbreviated author names (initials)
- Abbreviated journal names
- Compact format

### Journal Article Examples

**Single Author:**
```
[1] J. A. Smith, "The impact of artificial intelligence on cognitive development," 
    J. Cogn. Psychol., vol. 45, no. 3, pp. 234-256, 2020. 
    doi: 10.1234/jcp.2020.45.3.234.
```

**Two to Six Authors:**
```
[2] M. R. Johnson and K. L. Williams, "Machine learning approaches to natural language 
    processing," Comput. Linguist., vol. 38, no. 2, pp. 145-178, 2019. 
    doi: 10.1234/cl.2019.38.2.145.
```

**More Than Six Authors:**
```
[3] L. Chen et al., "Deep learning architectures for image recognition," Comput. Vis. 
    Res., vol. 52, no. 4, pp. 567-589, 2021. doi: 10.1234/cvr.2021.52.4.567.
```

### Conference Paper Examples

```
[4] R. Kumar and S. Lee, "Blockchain applications in healthcare systems," in Proc. 
    Int. Conf. Healthcare Technol., 2020, pp. 123-135. doi: 10.1234/icht.2020.123.
```

### Book Examples

**Entire Book:**
```
[5] R. A. Thompson, Cognitive Development in Early Childhood. Academic Press, 2018.
```

**Edited Book:**
```
[6] C. D. Martinez and E. F. Wilson, Eds., Advances in Machine Learning. MIT Press, 2019.
```

### Web Sources

```
[7] National Institute of Health, "Guidelines for ethical research practices," 2021. 
    [Online]. Available: https://www.nih.gov/research-ethics
```

### Inline Citation Examples

**Basic Citation:**
- Single reference: `[1]`
- Multiple references: `[1], [3], [5]`
- Range: `[1]-[5]`
- Combined: `[1], [3]-[5], [7]`

**In Text:**
- "As shown in [1], the results indicate..."
- "Multiple studies [1]-[3] have demonstrated..."
- "Smith et al. [1] proposed a method..."

## Inline Citations

### Comparison Across Styles

| Context | APA | MLA | Chicago | IEEE |
|---------|-----|-----|---------|------|
| Single author | (Smith, 2020) | (Smith 45) | (Smith 2020) | [1] |
| Two authors | (Smith & Jones, 2020) | (Smith and Jones 45) | (Smith and Jones 2020) | [1] |
| Three+ authors | (Smith et al., 2020) | (Smith et al. 45) | (Smith et al. 2020) | [1] |
| With page | (Smith, 2020, p. 45) | (Smith 45) | (Smith 2020, 45) | [1] |
| Multiple sources | (Smith, 2020; Jones, 2019) | (Smith 45; Jones 23) | (Smith 2020; Jones 2019) | [1], [2] |

### When to Use Inline Citations

1. **Direct Quotes**: Always cite with page numbers
   - APA: `(Smith, 2020, p. 45)`
   - MLA: `(Smith 45)`

2. **Paraphrasing**: Cite without page numbers
   - APA: `(Smith, 2020)`
   - MLA: `(Smith)`

3. **Multiple Ideas from Same Source**: Cite once at end of paragraph

4. **Common Knowledge**: No citation needed

## Bibliography Formatting

### General Rules

All styles use:
- **Hanging indent**: First line flush left, subsequent lines indented
- **Alphabetical order**: By first author's last name
- **Double spacing**: Between and within entries (in formal papers)

### APA Bibliography (References)

```
References

Chen, L., Rodriguez, A. M., & Patel, S. K. (2021). Deep learning architectures for 
    image recognition. Computer Vision Research, 52(4), 567-589. 
    https://doi.org/10.1234/cvr.2021.52.4.567

Johnson, M. R., & Williams, K. L. (2019). Machine learning approaches to natural 
    language processing. Computational Linguistics, 38(2), 145-178. 
    https://doi.org/10.1234/cl.2019.38.2.145

Smith, J. A. (2020). The impact of artificial intelligence on cognitive development. 
    Journal of Cognitive Psychology, 45(3), 234-256. 
    https://doi.org/10.1234/jcp.2020.45.3.234
```

### MLA Bibliography (Works Cited)

```
Works Cited

Chen, Li, et al. "Deep Learning Architectures for Image Recognition." Computer Vision 
    Research, vol. 52, no. 4, 2021, pp. 567-589. 
    https://doi.org/10.1234/cvr.2021.52.4.567.

Johnson, Mary R., and Karen L. Williams. "Machine Learning Approaches to Natural 
    Language Processing." Computational Linguistics, vol. 38, no. 2, 2019, pp. 145-178. 
    https://doi.org/10.1234/cl.2019.38.2.145.

Smith, John A. "The Impact of Artificial Intelligence on Cognitive Development." 
    Journal of Cognitive Psychology, vol. 45, no. 3, 2020, pp. 234-256. 
    https://doi.org/10.1234/jcp.2020.45.3.234.
```

### Chicago Bibliography

```
Bibliography

Chen, Li, Ana M. Rodriguez, and Sanjay K. Patel. 2021. "Deep Learning Architectures 
    for Image Recognition." Computer Vision Research 52, no. 4: 567-589. 
    https://doi.org/10.1234/cvr.2021.52.4.567.

Johnson, Mary R., and Karen L. Williams. 2019. "Machine Learning Approaches to Natural 
    Language Processing." Computational Linguistics 38, no. 2: 145-178. 
    https://doi.org/10.1234/cl.2019.38.2.145.

Smith, John A. 2020. "The Impact of Artificial Intelligence on Cognitive Development." 
    Journal of Cognitive Psychology 45, no. 3: 234-256. 
    https://doi.org/10.1234/jcp.2020.45.3.234.
```

### IEEE References

```
References

[1] L. Chen, A. M. Rodriguez, and S. K. Patel, "Deep learning architectures for image 
    recognition," Comput. Vis. Res., vol. 52, no. 4, pp. 567-589, 2021. 
    doi: 10.1234/cvr.2021.52.4.567.

[2] M. R. Johnson and K. L. Williams, "Machine learning approaches to natural language 
    processing," Comput. Linguist., vol. 38, no. 2, pp. 145-178, 2019. 
    doi: 10.1234/cl.2019.38.2.145.

[3] J. A. Smith, "The impact of artificial intelligence on cognitive development," 
    J. Cogn. Psychol., vol. 45, no. 3, pp. 234-256, 2020. 
    doi: 10.1234/jcp.2020.45.3.234.
```

## Special Cases

### No Author

**APA:**
```
[No author]. (2020). Climate change impacts. Environmental Portal. 
    https://www.envportal.org/climate
```

**MLA:**
```
"Climate Change Impacts." Environmental Portal, 2020. https://www.envportal.org/climate. 
    Accessed 15 Nov. 2024.
```

**Chicago:**
```
[No author]. 2020. "Climate Change Impacts." Environmental Portal. 
    https://www.envportal.org/climate.
```

**IEEE:**
```
[1] [No author], "Climate change impacts," Environmental Portal, 2020. [Online]. 
    Available: https://www.envportal.org/climate
```

### No Date

**APA:**
```
Smith, J. A. (n.d.). Research methods in psychology. Psychology Today. 
    https://www.psychtoday.com/methods
```

**MLA:**
```
Smith, John A. "Research Methods in Psychology." Psychology Today. 
    https://www.psychtoday.com/methods. Accessed 15 Nov. 2024.
```

**Chicago:**
```
Smith, John A. n.d. "Research Methods in Psychology." Psychology Today. 
    https://www.psychtoday.com/methods.
```

**IEEE:**
```
[1] J. A. Smith, "Research methods in psychology," Psychology Today. [Online]. 
    Available: https://www.psychtoday.com/methods
```

### Preprints (arXiv, bioRxiv)

**APA:**
```
Zhang, Y., & Liu, X. (2023). Novel approaches to quantum computing. arXiv. 
    https://arxiv.org/abs/2301.12345
```

**MLA:**
```
Zhang, Yu, and Xin Liu. "Novel Approaches to Quantum Computing." arXiv, 2023. 
    https://arxiv.org/abs/2301.12345.
```

**Chicago:**
```
Zhang, Yu, and Xin Liu. 2023. "Novel Approaches to Quantum Computing." arXiv. 
    https://arxiv.org/abs/2301.12345.
```

**IEEE:**
```
[1] Y. Zhang and X. Liu, "Novel approaches to quantum computing," arXiv, 2023. 
    [Online]. Available: https://arxiv.org/abs/2301.12345
```

### Incomplete Citations

When citation metadata is incomplete, Gazzali Research flags it:

```
Smith, J. (2020). Research findings. [Incomplete citation]
```

This indicates that some required fields (e.g., venue, page numbers) are missing.

## Usage in Gazzali Research

### Setting Citation Style

**Command Line:**
```bash
python -m gazzali.gazzali "your research question" \
    --academic \
    --citation-style apa
```

**Environment Variable:**
```bash
export CITATION_STYLE=mla
python -m gazzali.gazzali "your research question" --academic
```

### Available Options

- `apa` - APA 7th Edition (default)
- `mla` - MLA 9th Edition
- `chicago` - Chicago 17th Edition (author-date)
- `ieee` - IEEE Style

### Automatic Citation Tracking

Gazzali Research automatically:

1. **Captures citations** from all sources (Scholar, web pages, documents)
2. **Extracts metadata** (authors, year, title, venue, DOI)
3. **Formats inline citations** in your chosen style
4. **Generates bibliography** sorted alphabetically
5. **Flags incomplete citations** for review

### Exporting Citations

**BibTeX Export:**
```bash
python -m gazzali.gazzali "your research question" \
    --academic \
    --export-bib
```

This creates a `.bib` file in the output directory with all citations in BibTeX format.

**RIS Export:**

The citation manager also supports RIS format export for use with reference managers like Zotero, Mendeley, or EndNote.

### Programmatic Usage

```python
from gazzali.citation_manager import CitationManager, CitationStyle

# Initialize manager
manager = CitationManager()

# Create citation
citation = manager.create_citation_from_metadata(
    title="Machine Learning Fundamentals",
    authors=["Smith, John", "Doe, Jane"],
    year=2020,
    venue="Journal of AI Research",
    volume="15",
    issue="3",
    pages="123-145",
    doi="10.1234/jair.2020.15.3.123"
)

# Add to manager
cid = manager.add_citation(citation)

# Get inline citation
inline = manager.get_inline_citation(cid, CitationStyle.APA)
print(inline)  # (Smith & Doe, 2020)

# Generate bibliography
bibliography = manager.generate_bibliography(CitationStyle.APA)
print(bibliography)
```

## Best Practices

### 1. Choose the Right Style

- **APA**: Psychology, education, social sciences
- **MLA**: Literature, humanities, arts
- **Chicago**: History, arts, some humanities
- **IEEE**: Engineering, computer science, technology

### 2. Consistency

- Use the same style throughout your document
- Follow all formatting rules for that style
- Don't mix citation styles

### 3. Complete Information

- Provide as much metadata as possible
- Include DOIs when available
- Record access dates for web sources

### 4. Verification

- Review generated citations for accuracy
- Check for incomplete citation flags
- Verify author names and publication details

### 5. Updates

- Citation styles are periodically updated
- Gazzali Research implements current editions
- Check for system updates to get latest style rules

## Additional Resources

### Official Style Guides

- **APA**: [https://apastyle.apa.org/](https://apastyle.apa.org/)
- **MLA**: [https://style.mla.org/](https://style.mla.org/)
- **Chicago**: [https://www.chicagomanualofstyle.org/](https://www.chicagomanualofstyle.org/)
- **IEEE**: [https://ieeeauthorcenter.ieee.org/](https://ieeeauthorcenter.ieee.org/)

### Citation Management Tools

- Zotero: [https://www.zotero.org/](https://www.zotero.org/)
- Mendeley: [https://www.mendeley.com/](https://www.mendeley.com/)
- EndNote: [https://endnote.com/](https://endnote.com/)

### Gazzali Research Documentation

- [Academic Mode Guide](ACADEMIC_MODE.md)
- [Output Formats](OUTPUT_FORMATS.md)
- [Discipline Settings](DISCIPLINE_SETTINGS.md)

---

**Note**: This documentation reflects the citation formatting implemented in Gazzali Research v1.0. For the most current style guidelines, always consult the official style manuals listed above.
