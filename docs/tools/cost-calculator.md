# Cost Calculator

Estimate the cost of implementing RAG patterns in your production system.

## Interactive Calculator

<div style="background: #f5f5f5; padding: 2rem; border-radius: 8px; margin: 2rem 0;">

### Input Your Parameters

<div style="margin: 1rem 0;">
  <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Monthly Query Volume</label>
  <input type="number" id="queryVolume" value="100000" min="1000" step="10000"
         style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;"
         onchange="calculateCosts()">
  <small style="color: #666;">Number of queries per month</small>
</div>

<div style="margin: 1rem 0;">
  <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Average Document Length</label>
  <input type="number" id="docLength" value="5000" min="100" step="500"
         style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;"
         onchange="calculateCosts()">
  <small style="color: #666;">Average characters per document</small>
</div>

<div style="margin: 1rem 0;">
  <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">LLM Model</label>
  <select id="llmModel" style="width: 100%; padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px;"
          onchange="calculateCosts()">
    <option value="gpt-3.5">GPT-3.5 Turbo ($0.001/1K input, $0.002/1K output)</option>
    <option value="gpt-4">GPT-4 ($0.03/1K input, $0.06/1K output)</option>
    <option value="claude-haiku">Claude 3 Haiku ($0.00025/1K input, $0.00125/1K output)</option>
    <option value="claude-sonnet" selected>Claude 3.5 Sonnet ($0.003/1K input, $0.015/1K output)</option>
  </select>
</div>

### Select Patterns to Use

<div style="margin: 1rem 0;">
  <label style="display: flex; align-items: center; margin: 0.5rem 0;">
    <input type="checkbox" id="semanticChunking" checked onchange="calculateCosts()"
           style="margin-right: 0.5rem; width: 20px; height: 20px;">
    <span>Semantic Chunking (one-time preprocessing)</span>
  </label>

  <label style="display: flex; align-items: center; margin: 0.5rem 0;">
    <input type="checkbox" id="hyde" onchange="calculateCosts()"
           style="margin-right: 0.5rem; width: 20px; height: 20px;">
    <span>HyDE (adds LLM call for hypothesis generation)</span>
  </label>

  <label style="display: flex; align-items: center; margin: 0.5rem 0;">
    <input type="checkbox" id="reranking" checked onchange="calculateCosts()"
           style="margin-right: 0.5rem; width: 20px; height: 20px;">
    <span>Re-ranking (cross-encoder inference)</span>
  </label>

  <label style="display: flex; align-items: center; margin: 0.5rem 0;">
    <input type="checkbox" id="metadataFiltering" checked onchange="calculateCosts()"
           style="margin-right: 0.5rem; width: 20px; height: 20px;">
    <span>Metadata Filtering (minimal overhead)</span>
  </label>

  <label style="display: flex; align-items: center; margin: 0.5rem 0;">
    <input type="checkbox" id="queryDecomp" onchange="calculateCosts()"
           style="margin-right: 0.5rem; width: 20px; height: 20px;">
    <span>Query Decomposition (3x LLM calls average)</span>
  </label>
</div>

<button onclick="calculateCosts()"
        style="background: #1e88e5; color: white; padding: 0.75rem 2rem; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; font-weight: 600; margin-top: 1rem;">
  Calculate Costs
</button>

<div id="results" style="margin-top: 2rem; display: none;">
  <h3 style="margin-bottom: 1rem;">Monthly Cost Estimate</h3>

  <div style="background: white; padding: 1.5rem; border-radius: 8px; border: 2px solid #1e88e5; margin-bottom: 1rem;">
    <div style="font-size: 2rem; font-weight: 700; color: #1e88e5;" id="totalCost">$0</div>
    <div style="color: #666;">Total Monthly Cost</div>
  </div>

  <table style="width: 100%; border-collapse: collapse;">
    <thead>
      <tr style="background: #f0f0f0;">
        <th style="padding: 0.75rem; text-align: left; border-bottom: 2px solid #ddd;">Component</th>
        <th style="padding: 0.75rem; text-align: right; border-bottom: 2px solid #ddd;">Cost</th>
      </tr>
    </thead>
    <tbody id="costBreakdown">
      <!-- Populated by JavaScript -->
    </tbody>
  </table>

  <div style="margin-top: 2rem; padding: 1rem; background: #e3f2fd; border-left: 4px solid #1e88e5; border-radius: 4px;">
    <strong>💡 Optimization Tips:</strong>
    <ul style="margin: 0.5rem 0 0 0;">
      <li>Use caching to reduce repeat queries by 30-50%</li>
      <li>Switch to Claude Haiku for 10x cost savings on simple queries</li>
      <li>Batch similar queries for better throughput</li>
      <li>Use metadata filtering to reduce search space (faster + cheaper)</li>
    </ul>
  </div>

  <div id="recommendations" style="margin-top: 1rem; padding: 1rem; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
    <!-- Populated by JavaScript -->
  </div>
</div>

</div>

<script>
function calculateCosts() {
  const volume = parseInt(document.getElementById('queryVolume').value);
  const docLength = parseInt(document.getElementById('docLength').value);
  const model = document.getElementById('llmModel').value;

  const patterns = {
    semanticChunking: document.getElementById('semanticChunking').checked,
    hyde: document.getElementById('hyde').checked,
    reranking: document.getElementById('reranking').checked,
    metadataFiltering: document.getElementById('metadataFiltering').checked,
    queryDecomp: document.getElementById('queryDecomp').checked
  };

  // Model pricing (per 1K tokens)
  const pricing = {
    'gpt-3.5': { input: 0.001, output: 0.002 },
    'gpt-4': { input: 0.03, output: 0.06 },
    'claude-haiku': { input: 0.00025, output: 0.00125 },
    'claude-sonnet': { input: 0.003, output: 0.015 }
  };

  const prices = pricing[model];
  const avgTokens = docLength / 4; // Rough token estimate

  let costs = {
    embeddings: 20, // Base embedding cost
    vectorDB: 50, // Base vector DB cost
    llmGeneration: 0,
    preprocessing: 0,
    reranking: 0,
    additional: 0
  };

  // LLM generation (per query)
  const inputTokens = 2000; // Context + query
  const outputTokens = 400; // Answer
  costs.llmGeneration = (volume * (inputTokens * prices.input + outputTokens * prices.output)) / 1000;

  // Pattern costs
  if (patterns.semanticChunking) {
    costs.preprocessing += 100; // One-time embedding cost for chunking
  }

  if (patterns.hyde) {
    // Extra LLM call per query for hypothesis
    const hydeTokens = 200;
    costs.additional += (volume * hydeTokens * (prices.input + prices.output)) / 1000;
  }

  if (patterns.reranking) {
    // Cross-encoder inference cost
    costs.reranking += volume * 0.0001; // $0.0001 per query
  }

  if (patterns.metadataFiltering) {
    // Minimal overhead
    costs.additional += 5;
  }

  if (patterns.queryDecomp) {
    // 3x LLM calls on average (decompose + retrieve each)
    const decompTokens = 600;
    costs.additional += (volume * decompTokens * (prices.input + prices.output)) / 1000;
  }

  const total = Object.values(costs).reduce((a, b) => a + b, 0);

  // Display results
  document.getElementById('results').style.display = 'block';
  document.getElementById('totalCost').textContent = '$' + total.toFixed(2);

  const breakdown = document.getElementById('costBreakdown');
  breakdown.innerHTML = `
    <tr>
      <td style="padding: 0.75rem; border-bottom: 1px solid #ddd;">Embeddings</td>
      <td style="padding: 0.75rem; text-align: right; border-bottom: 1px solid #ddd;">$${costs.embeddings.toFixed(2)}</td>
    </tr>
    <tr>
      <td style="padding: 0.75rem; border-bottom: 1px solid #ddd;">Vector Database</td>
      <td style="padding: 0.75rem; text-align: right; border-bottom: 1px solid #ddd;">$${costs.vectorDB.toFixed(2)}</td>
    </tr>
    <tr>
      <td style="padding: 0.75rem; border-bottom: 1px solid #ddd;">LLM Generation</td>
      <td style="padding: 0.75rem; text-align: right; border-bottom: 1px solid #ddd;">$${costs.llmGeneration.toFixed(2)}</td>
    </tr>
    ${costs.preprocessing > 0 ? `
    <tr>
      <td style="padding: 0.75rem; border-bottom: 1px solid #ddd;">Preprocessing (one-time)</td>
      <td style="padding: 0.75rem; text-align: right; border-bottom: 1px solid #ddd;">$${costs.preprocessing.toFixed(2)}</td>
    </tr>` : ''}
    ${costs.reranking > 0 ? `
    <tr>
      <td style="padding: 0.75rem; border-bottom: 1px solid #ddd;">Re-ranking</td>
      <td style="padding: 0.75rem; text-align: right; border-bottom: 1px solid #ddd;">$${costs.reranking.toFixed(2)}</td>
    </tr>` : ''}
    ${costs.additional > 0 ? `
    <tr>
      <td style="padding: 0.75rem; border-bottom: 1px solid #ddd;">Pattern Overhead</td>
      <td style="padding: 0.75rem; text-align: right; border-bottom: 1px solid #ddd;">$${costs.additional.toFixed(2)}</td>
    </tr>` : ''}
  `;

  // Recommendations
  const recommendations = document.getElementById('recommendations');
  let recText = '<strong>⚡ Recommendations:</strong><ul style="margin: 0.5rem 0 0 0;">';

  if (total > 1000) {
    recText += '<li>Consider caching - can reduce costs by 30-50%</li>';
    recText += '<li>Use cheaper models for initial processing</li>';
  }

  if (patterns.queryDecomp && patterns.hyde) {
    recText += '<li>HyDE + Query Decomposition is redundant - pick one</li>';
  }

  if (!patterns.metadataFiltering) {
    recText += '<li>Add metadata filtering - minimal cost, big quality gain</li>';
  }

  recText += '</ul>';
  recommendations.innerHTML = recText;
}

// Calculate on load
window.addEventListener('load', calculateCosts);
</script>

## Cost Breakdown by Pattern

### Semantic Chunking
**One-time cost**: ~$100-200 for embedding chunks
**Ongoing**: Storage only (~$2-5/month)
**ROI**: High - improves all downstream queries

### HyDE
**Per query**: +$0.0002-0.0006 depending on model
**100K queries/month**: ~$20-60
**ROI**: Medium-High for Q&A systems

### Re-ranking
**Per query**: ~$0.0001
**100K queries/month**: ~$10
**ROI**: Very High - massive quality improvement for low cost

### Metadata Filtering
**Overhead**: Negligible (~$5/month for storage)
**Actually saves money**: Smaller search space = faster = cheaper
**ROI**: Excellent - often pays for itself

### Query Decomposition
**Per query**: +$0.0006-0.0018 depending on model
**100K queries/month**: ~$60-180
**ROI**: Medium - high value for complex queries only

## Real-World Examples

### Startup (10K queries/month)

**Basic Stack**: Semantic Chunking + Metadata Filtering + Claude Haiku
- **Cost**: ~$50/month
- **Quality**: Good for most use cases
- **Recommendation**: Great starting point

### Mid-Size (100K queries/month)

**Enhanced Stack**: Semantic + Metadata + Re-ranking + Claude Sonnet
- **Cost**: ~$400/month
- **Quality**: High precision
- **Recommendation**: Production standard

### Enterprise (1M queries/month)

**Full Stack**: All patterns + caching + Claude Sonnet
- **Cost**: ~$3,000-4,000/month (with optimizations)
- **Quality**: Highest
- **Recommendation**: Mission-critical applications

## Optimization Strategies

### 1. Model Selection
- Use Haiku for simple queries → 10x cost savings
- Use Sonnet only for complex queries
- Route intelligently based on query complexity

### 2. Caching
- Cache common queries → 30-50% cost reduction
- Use Redis or similar
- Set appropriate TTL based on content freshness needs

### 3. Batching
- Process similar queries together
- Reduce API call overhead
- Better throughput

### 4. Smart Retrieval
- Use metadata filtering to reduce search space
- Retrieve fewer candidates, re-rank more precisely
- Don't over-retrieve

### 5. Monitoring
- Track cost per query
- Identify expensive queries
- Optimize hot paths

## Try the Calculator

Use the interactive calculator above to estimate your costs based on:
- Your expected query volume
- Document sizes
- Pattern selection
- LLM model choice

Get instant recommendations for cost optimization!

---

**Questions about costs?** Check the [Pattern Comparison](comparison.md) for detailed analysis or [open an issue](https://github.com/PeteSumners/rag-showroom/issues).
