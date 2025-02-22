from flask import Flask, jsonify, request
import statistics
import math
import os
app = Flask(__name__)

# Complex trend analysis function
def analyze_sales_trend(monthly_sales, customer_segments=None):
    if not monthly_sales or len(monthly_sales) < 3:
        return {
            "avg_sales": 0,
            "trend": "insufficient data",
            "growth_rate": 0,
            "volatility": 0,
            "momentum": 0,
            "dominant_segment": None
        }

    # Basic metrics
    avg_sales = sum(monthly_sales) / len(monthly_sales)

    # Growth rate (average percentage change)
    growth_rates = [(monthly_sales[i] - monthly_sales[i-1]) / monthly_sales[i-1] 
                    for i in range(1, len(monthly_sales)) if monthly_sales[i-1] != 0]
    avg_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0

    # Volatility (standard deviation of growth rates)
    volatility = statistics.stdev(growth_rates) if len(growth_rates) > 1 else 0

    # Recent momentum (weighted average of last 3 months, more weight to recent)
    recent_sales = monthly_sales[-3:] if len(monthly_sales) >= 3 else monthly_sales
    weights = [1, 2, 3][:len(recent_sales)]
    momentum = sum(s * w for s, w in zip(recent_sales, weights)) / sum(weights) if recent_sales else 0
    momentum_direction = "positive" if momentum > avg_sales else "negative"

    # Trend classification
    if avg_growth_rate > 0.05 and volatility < 0.1:
        trend = "strong growth"
    elif avg_growth_rate > 0:
        trend = "moderate growth"
    elif avg_growth_rate < -0.05 and volatility > 0.15:
        trend = "sharp decline"
    elif avg_growth_rate < 0:
        trend = "moderate decline"
    else:
        trend = "stable"

    # Dominant segment (if provided)
    dominant_segment = max(customer_segments, key=customer_segments.get) if customer_segments else None

    return {
        "avg_sales": avg_sales,
        "trend": trend,
        "growth_rate": avg_growth_rate,
        "volatility": volatility,
        "momentum": momentum_direction,
        "dominant_segment": dominant_segment
    }

# 1. Sales Recommendations Endpoint
@app.route('/sales-recommendations', methods=['POST'])
def get_sales_recommendations():
    data = request.get_json()
    if not data or 'monthly_sales' not in data or 'product_features' not in data:
        return jsonify({"error": "Please provide monthly_sales and product_features"}), 400

    monthly_sales = data['monthly_sales']
    product_features = data['product_features']
    customer_segments = data.get('customer_segments', None)
    analysis = analyze_sales_trend(monthly_sales, customer_segments)

    trend = analysis['trend']
    momentum = analysis['momentum']
    volatility = analysis['volatility']
    dominant_segment = analysis['dominant_segment']

    if trend in ["strong growth", "moderate growth"]:
        recommendations = [
            f"Leverage {trend} with a 'Caregiver Elite' edition featuring next-gen {product_features[0]}.",
            "Host a 'Dementia Tech Fest' to amplify buzz, targeting trending regions.",
            "Launch a 'Momentum Bundle' with family sync features for growing demand.",
            "Partner with AI health platforms for scalable integrations amid rising sales.",
            "Offer a 'Growth Reward' cashback for bulk buys, riding high momentum.",
            "Create a gamified app for caregivers with real-time MemoTag insights.",
            "Expand globally with localized AI voices, capitalizing on stable growth.",
            "Sell limited-edition 'Hope Bands' with proceeds to dementia research.",
            "Upsell a predictive care subscription if momentum is {momentum}.",
            "Run a viral campaign with caregivers showcasing MemoTag success stories."
        ]
    elif trend in ["sharp decline", "moderate decline"]:
        recommendations = [
            f"Counter {trend} with a 'Caregiver lifeline' discount on {product_features[0]}.",
            "Pivot to a rental model to lower barriers during volatile {volatility:.2f} sales.",
            "Launch a 'Memory Guardians' referral program to rebuild trust.",
            "Host free AI caregiving webinars to re-engage amid {momentum} momentum.",
            "Introduce a 'Core Care' low-cost version to recapture lost sales.",
            "Donate excess stock to dementia clinics, boosting goodwill in decline.",
            "Offer a 'Revival Trade-In' for old MemoTags to spark renewals.",
            "Focus retention with a free AI care tips app tied to {product_features[-1]}.",
            "Test hyper-local ads in {dominant_segment or 'key'} segment regions.",
            "Bundle with affordable add-ons to counter declining trends."
        ]
    else:  # stable
        recommendations = [
            "Stabilize sales with a 'Steady Care' subscription blending all features.",
            "Launch a 'Caregiver Stories' podcast to maintain steady engagement.",
            "Offer a 'Family Care Kit' with consistent pricing for steady demand.",
            "Partner with steady-state care homes for bulk MemoTag adoption.",
            "Introduce a loyalty points system for consistent buyers.",
            "Create a 'Memory Moments' AR feature to keep interest alive.",
            "Test a mid-tier model with balanced {product_features[0]} access.",
            "Run steady-state campaigns with caregivers as brand ambassadors.",
            "Upsell a 'Care Insights' dashboard for stable user growth.",
            "Host a virtual 'Dementia Care Day' to reinforce brand reliability."
        ]
    return jsonify({"recommendations": recommendations})

# 2. Sales Strategies Endpoint
@app.route('/sales-strategies', methods=['POST'])
def get_sales_strategies():
    data = request.get_json()
    if not data or 'monthly_sales' not in data:
        return jsonify({"error": "Please provide monthly_sales"}), 400

    monthly_sales = data['monthly_sales']
    customer_segments = data.get('customer_segments', None)
    total_sales = data.get('total_sales', 0)
    analysis = analyze_sales_trend(monthly_sales, customer_segments)

    trend = analysis['trend']
    dominant_segment = analysis['dominant_segment'] or "key customers"

    if trend in ["strong growth", "moderate growth"]:
        strategies = [
            f"Scale B2B to {dominant_segment} with bulk deals for care facilities.",
            "Launch a premium tier with predictive AI alerts to ride {trend}.",
            "Expand neurologist trials, leveraging growth for clinical credibility."
        ]
    elif trend in ["sharp decline", "moderate decline"]:
        strategies = [
            f"Retarget {dominant_segment} with loyalty offers to reverse {trend}.",
            "Shift to a low-entry subscription to stabilize cash flow in decline.",
            "Build grassroots trust with dementia NGOs amid volatile sales."
        ]
    else:  # stable
        strategies = [
            f"Solidify {dominant_segment} with steady B2B partnerships.",
            "Introduce a balanced tiered pricing for consistent revenue.",
            "Collaborate with steady-state health forums for brand reinforcement."
        ]
    return jsonify({"strategies": strategies})

# 3. Marketing Funnels Endpoint
@app.route('/marketing-funnels', methods=['POST'])
def get_marketing_funnels():
    data = request.get_json()
    if not data or 'product_features' not in data:
        return jsonify({"error": "Please provide product_features"}), 400

    product_features = data['product_features']
    funnels = [
        "AI caregiving blog → Webinar on dementia tech → MemoTag trial.",
        "Caregiver testimonials on social → Emotional landing page → Subscription.",
        "VR demo at health expos → QR code trial → Purchase CTA.",
        "Podcast on aging tech → Whitepaper on AI wearables → Email nurture.",
        "Ads to adult children → Virtual family consult → AI-driven sale."
    ]
    return jsonify({"funnels": funnels})

# Root endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to MemoTag API",
        "endpoints": ["/sales-recommendations", "/sales-strategies", "/marketing-funnels"],
        "note": "POST with JSON: monthly_sales (required), total_sales, customer_segments, product_features"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
