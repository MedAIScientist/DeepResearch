# Scholar-First Search Strategy

## Overview

The Scholar-First Search Strategy is a core feature of Gazzali Research's academic mode that prioritizes peer-reviewed academic sources over general web content. This strategy ensures that research is grounded in scholarly literature and meets academic standards for credibility and rigor.

## How It Works

### 1. Tool Prioritization

In academic mode, the research agent follows this search hierarchy:

1. **Google Scholar** (Primary) - Always searched first for peer-reviewed sources
2. **Visit Tool** (Secondary) - Used to access full paper content and extract detailed information
3. **General Search** (Supplementary) - Used only after Scholar search for additional context

### 2. Source Quality Scoring

Every source is automatically assessed using a 0-10 quality scale:

| Source Type | Quality Score | Description |
|-------------|---------------|-------------|
| Peer-reviewed journal/conference | 10 | Highest quality - undergone rigorous peer review |
| Academic institution/university | 8 | High quality - from recognized educational institutions |
| Government/research organization | 7 | High quality - from official research agencies |
| Professional organization | 6 | Medium-high quality - from established professional bodies |
| Reputable news source | 5 | Medium quality - journalistic standards applied |
| General web content | 3 | Low quality - no formal review process |
| Unknown/unverified | 2 | Lowest quality - credibility uncertain |

### 3. Quality Filtering

Sources are filtered based on configurable quality thresholds:

- **Default threshold**: 7/10 (academic institutions and above)
- **Configurable**: Set via `SOURCE_QUALITY_THRESHOLD` environment variable
- **Warnings**: Low-quality sources trigger automatic warnings
- **Suggestions**: Agent receives suggestions to use Scholar tool when using general search

### 4. Quality Metrics Tracking

The system tracks and reports:

- **Average quality score** for each tool call
- **Peer-reviewed source count** vs. total sources
- **Quality level** (high/medium/low) for each result set
- **Tool usage** (Scholar vs. general search)

## Configuration

### Environment Variables

```bash
# Enable academic mode (required for Scholar-first strategy)
GAZZALI_ACADEMIC_MODE=true

# Enable Scholar priority (default: true)
SCHOLAR_PRIORITY=true

# Set minimum quality threshold (0-10, default: 7)
SOURCE_QUALITY_THRESHOLD=7

# Set minimum peer-reviewed sources (default: 5)
MIN_PEER_REVIEWED_SOURCES=5
```

### Command-Line Flags

```bash
# Enable academic mode with Scholar-first strategy
python -m gazzali.gazzali "your research question" --academic

# Customize quality threshold
SOURCE_QUALITY_THRESHOLD=8 python -m gazzali.gazzali "your question" --academic
```

## Example Workflow

### Standard Academic Research

```
1. User asks: "What are the effects of climate change on coral reefs?"

2. Agent receives academic mode prompt with Scholar-first instructions

3. Agent calls google_scholar tool:
   - Query: "climate change effects coral reefs"
   - Returns: 10 peer-reviewed papers
   - Quality assessment: 10/10 (high), 10 peer-reviewed sources

4. Agent calls visit tool on key papers:
   - Extracts full methodology and findings
   - Quality assessment: 10/10 (high), peer-reviewed

5. Agent calls search tool for supplementary info:
   - Query: "recent coral reef conservation efforts"
   - Quality assessment: 5/10 (medium), 0 peer-reviewed
   - Warning: "Consider using google_scholar for academic sources"

6. Agent synthesizes findings prioritizing high-quality sources
```

### Quality Warning Example

When the agent uses general search without Scholar:

```
📊 Source Quality Assessment:
   Tool: search
   Quality Score: 3/10 (low)
   Peer-Reviewed Sources: 0/5

⚠️  SOURCE QUALITY WARNING: Average quality score (3/10) is below 
threshold (7/10). These sources may not meet academic standards. 
Consider using google_scholar tool for peer-reviewed sources.

💡 ACADEMIC MODE SUGGESTION: Consider using google_scholar tool 
instead of search for academic sources. Scholar provides peer-reviewed 
papers with citation metadata.
Example: google_scholar(query="your search terms")
```

## Benefits

### 1. Higher Quality Research

- **Peer-reviewed sources**: Ensures information has undergone scholarly review
- **Citation metadata**: Automatic extraction of authors, years, venues, DOIs
- **Credibility**: Prioritizes recognized academic publishers and institutions

### 2. Academic Standards Compliance

- **Proper attribution**: All sources tracked with full bibliographic data
- **Methodology transparency**: Research methods documented from papers
- **Evidence hierarchy**: Sources ranked by academic credibility

### 3. Efficiency

- **Targeted search**: Scholar tool optimized for academic queries
- **Reduced noise**: Filters out low-quality web content
- **Better citations**: Automatic citation count and impact metrics

### 4. Transparency

- **Quality metrics**: Clear scoring for every source
- **Source tracking**: Complete record of all sources consulted
- **Warnings**: Explicit alerts when quality is below threshold

## Best Practices

### For Users

1. **Enable academic mode** for scholarly research: `--academic` flag
2. **Set appropriate thresholds** based on your field's standards
3. **Review quality metrics** in the output to assess source credibility
4. **Adjust thresholds** if too restrictive or too permissive

### For Researchers

1. **Start with Scholar**: Always begin with google_scholar tool
2. **Use multiple queries**: Try different search terms for comprehensive coverage
3. **Visit key papers**: Use visit tool to access full paper content
4. **Supplement carefully**: Use general search only for context, not primary evidence
5. **Check quality scores**: Monitor quality assessments to ensure standards are met

## Technical Implementation

### Source Quality Assessment

The `assess_source_quality()` method in `react_agent.py` evaluates sources based on:

- **Tool type**: Scholar tool results automatically scored 10/10
- **URL patterns**: Detects .edu, .gov, academic publishers
- **Content analysis**: Identifies academic indicators (DOI, journal names, etc.)
- **Citation metadata**: Presence of proper bibliographic information

### Quality Filtering

The `filter_low_quality_sources()` method:

- Compares quality score to threshold
- Adds warnings for below-threshold sources
- Preserves all content (no deletion, only annotation)
- Provides actionable suggestions

### Scholar Suggestions

The `suggest_scholar_search()` method:

- Detects when general search is used
- Provides specific Scholar query examples
- Only activates in academic mode with Scholar priority enabled

## Troubleshooting

### Issue: Too many quality warnings

**Solution**: Lower the `SOURCE_QUALITY_THRESHOLD`:
```bash
SOURCE_QUALITY_THRESHOLD=5 python -m gazzali.gazzali "question" --academic
```

### Issue: Not enough sources found

**Solution**: 
1. Try broader search terms
2. Use multiple Scholar queries with different keywords
3. Temporarily lower quality threshold for exploratory research

### Issue: Scholar tool not being used

**Solution**: 
1. Verify `GAZZALI_ACADEMIC_MODE=true` is set
2. Check that `SCHOLAR_PRIORITY=true` (default)
3. Ensure academic prompts are loaded (check for "🎓 Academic Mode" message)

### Issue: General search used before Scholar

**Solution**: The agent makes autonomous decisions, but:
1. Academic prompts explicitly instruct Scholar-first
2. Quality warnings will alert to low-quality sources
3. Suggestions will recommend Scholar tool usage

## Related Documentation

- [Academic Mode Guide](ACADEMIC_MODE.md) - Complete academic features overview
- [Citation Management](CITATION_MANAGER.md) - Citation tracking and formatting
- [Scholar Tool](SCHOLAR_TOOL.md) - Google Scholar integration details
- [Agent Integration](AGENT_INTEGRATION.md) - How academic mode affects agent behavior

## References

This strategy implements requirements:
- **Requirement 1.1**: Prioritize academic sources over general web content
- **Requirement 1.2**: Utilize Scholar Tool before general web searches
- **Requirement 7.1**: Evaluate source credibility and quality

## Version History

- **v1.0** (2024): Initial implementation of Scholar-first strategy
  - Source quality scoring system
  - Automatic quality assessment
  - Quality filtering and warnings
  - Scholar tool suggestions
