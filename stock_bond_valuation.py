import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import random

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Stock & Bond Valuation Lab",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def currency(x):
    return f"₹{x:,.2f}"

def pct(x):
    return f"{round(x, 4)}%"

# =========================================================
# TITLE
# =========================================================

st.title("📈 Experiential Learning Lab: Stock & Bond Valuation")

st.markdown("""
Welcome to the experiential finance learning platform for **Security Valuation**.

This app teaches:

- Bond Valuation & Pricing
- Yield to Maturity (YTM)
- Duration & Convexity
- Dividend Discount Models (DDM)
- Gordon Growth Model
- Free Cash Flow to Equity (FCFE)
- Price/Earnings & Market Multiples
- CAPM & Required Return
- Relative Valuation

through:

✅ Practical financial decisions  
✅ Real-world Indian market examples  
✅ Interactive simulations  
✅ Step-by-step solvers  
✅ Quiz engine with hints  
✅ Common student mistakes  
✅ Formula cheat sheet
""")

# =========================================================
# SIDEBAR
# =========================================================

menu = st.sidebar.radio(
    "Choose Module",
    [
        "Introduction",
        # ── BOND VALUATION ──────────────────────────────
        "Bond Basics & Terminology",
        "Bond Valuation",
        "Yield to Maturity (YTM)",
        "Bond Price-Yield Relationship",
        "Duration & Convexity",
        "Types of Bonds",
        # ── STOCK VALUATION ─────────────────────────────
        "Stock Basics & Terminology",
        "Dividend Discount Model (DDM)",
        "Gordon Growth Model",
        "Multi-Stage DDM",
        "Free Cash Flow to Equity (FCFE)",
        "Price Multiples & Relative Valuation",
        # ── REQUIRED RETURN ─────────────────────────────
        "CAPM & Required Return",
        "Risk Premium & Beta",
        # ── TOOLS ───────────────────────────────────────
        "Valuation Decision Tool",
        "Step-by-Step Solver",
        "AI Hint System",
        "Quiz Engine",
        "Excel Formula Trainer",
        "Formula Cheat Sheet",
        "Common Student Mistakes",
        "Advanced Quiz Bank",
        "Progress Tracker",
        "Case-Based Learning",
    ]
)

# =========================================================
# INTRODUCTION
# =========================================================

if menu == "Introduction":

    st.header("📘 Introduction to Security Valuation")

    st.markdown("""
## Core Question

**What is the right price for a stock or bond?**

Valuation answers:

- Is this stock overpriced or underpriced?
- Should I buy this bond at ₹950 or ₹1,050?
- What return can I expect from this investment?
- How does interest rate risk affect my bond portfolio?

---

## Two Asset Classes
""")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
**🏦 BONDS (Fixed Income)**

- Fixed coupon payments
- Principal returned at maturity
- Inverse price-yield relationship
- Credit risk & interest rate risk
- Duration measures sensitivity
        """)

    with col2:
        st.success("""
**📈 STOCKS (Equity)**

- Uncertain future dividends/cash flows
- No maturity date
- Residual claim on assets
- Market sentiment + fundamentals
- Multiple valuation approaches
        """)

    st.markdown("""
---

## Fundamental Principle

> **Value = Present Value of all future cash flows discounted at the required rate of return**

This single principle powers:
- Bond pricing (known cash flows)
- DDM (expected dividends)
- FCFE (free cash flows to equity)
- All DCF-based valuations
""")

    st.info("""
**Indian Market Context:**
- NSE/BSE listed equities
- Government Securities (G-Secs)
- Corporate bonds (AAA to BBB rated)
- RBI repo rate influences discount rates
- Nifty 50 historical return ≈ 12-14% CAGR
""")

# =========================================================
# BOND BASICS & TERMINOLOGY
# =========================================================

elif menu == "Bond Basics & Terminology":

    st.header("🏦 Bond Basics & Terminology")

    st.markdown("""
A **bond** is a loan made by an investor to a borrower (corporate or government).
The borrower promises to pay:
1. Periodic **coupon payments** (interest)
2. **Face value (par value)** at maturity
""")

    terms = pd.DataFrame({
        "Term": [
            "Face Value (Par Value)",
            "Coupon Rate",
            "Coupon Payment",
            "Maturity",
            "Current Price",
            "Yield to Maturity (YTM)",
            "Premium Bond",
            "Discount Bond",
            "Par Bond",
            "Clean Price",
            "Dirty Price",
            "Accrued Interest",
        ],
        "Definition": [
            "Principal amount repaid at maturity (typically ₹1,000 or ₹100)",
            "Annual interest rate stated on bond (% of face value)",
            "Coupon Rate × Face Value (annual or semi-annual)",
            "Date when principal is repaid to bondholder",
            "Market price — may differ from face value",
            "Discount rate that equates PV of cash flows to current price",
            "Bond trading above face value (YTM < Coupon Rate)",
            "Bond trading below face value (YTM > Coupon Rate)",
            "Bond trading at face value (YTM = Coupon Rate)",
            "Quoted price excluding accrued interest",
            "Clean Price + Accrued Interest (actual settlement price)",
            "Interest earned since last coupon date",
        ]
    })

    st.table(terms)

    st.subheader("📐 Visual: Cash Flow Timeline")

    st.markdown("""
For a ₹1,000 face value, 8% coupon, 3-year bond:

```
Year:     0          1          2          3
          |          |          |          |
Cash:   −Price    +₹80       +₹80     +₹80 + ₹1,000
```

The investor pays the price today and receives coupons + face value.
""")

    face = 1000
    coupon_rate = 8.0
    years = 3
    coupon = face * coupon_rate / 100

    cfs = [coupon] * years
    cfs[-1] += face
    cf_years = list(range(1, years + 1))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cf_years,
        y=cfs,
        text=[f"₹{c:,.0f}" for c in cfs],
        textposition='outside',
        marker_color=['#185FA5'] * (years - 1) + ['#3B6D11'],
        name="Cash Inflows"
    ))
    fig.update_layout(
        title="Bond Cash Flow Timeline (₹1,000 par, 8% coupon, 3 years)",
        xaxis_title="Year",
        yaxis_title="Cash Flow (₹)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# BOND VALUATION
# =========================================================

elif menu == "Bond Valuation":

    st.header("💰 Bond Valuation")

    st.markdown("""
## Formula

$$P = \\sum_{t=1}^{n} \\frac{C}{(1+r)^t} + \\frac{F}{(1+r)^n}$$

Where:
- **P** = Bond price
- **C** = Coupon payment per period
- **F** = Face value
- **r** = Required rate of return per period
- **n** = Number of periods
""")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        face = st.number_input("Face Value (₹)", value=1000.0, min_value=100.0)
    with col2:
        coupon_rate = st.number_input("Coupon Rate (%)", value=8.0, min_value=0.0, max_value=30.0)
    with col3:
        n = int(st.number_input("Years to Maturity", value=5, min_value=1, step=1))
    with col4:
        freq = st.selectbox("Coupon Frequency", ["Annual", "Semi-Annual"])

    ytm_input = st.number_input("Required Return / YTM (%)", value=10.0, min_value=0.01, max_value=50.0)

    if freq == "Semi-Annual":
        periods = n * 2
        r = ytm_input / 100 / 2
        coupon = face * coupon_rate / 100 / 2
    else:
        periods = n
        r = ytm_input / 100
        coupon = face * coupon_rate / 100

    # Calculate price
    pv_coupons = coupon * (1 - (1 + r) ** (-periods)) / r
    pv_face = face / (1 + r) ** periods
    price = pv_coupons + pv_face

    # Status
    if abs(price - face) < 0.01:
        status = "Par Bond (Price = Face Value)"
        color = "info"
    elif price > face:
        status = f"Premium Bond (Price > Face Value) — YTM < Coupon Rate"
        color = "success"
    else:
        status = f"Discount Bond (Price < Face Value) — YTM > Coupon Rate"
        color = "warning"

    st.success(f"**Bond Price = {currency(price)}**")

    if color == "success":
        st.success(status)
    elif color == "warning":
        st.warning(status)
    else:
        st.info(status)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("PV of Coupons", currency(pv_coupons))
    with col2:
        st.metric("PV of Face Value", currency(pv_face))
    with col3:
        st.metric("Total Price", currency(price))

    # Price breakdown chart
    fig = go.Figure(go.Pie(
        labels=["PV of Coupons", "PV of Face Value"],
        values=[pv_coupons, pv_face],
        marker_colors=["#185FA5", "#3B6D11"],
        hole=0.4
    ))
    fig.update_layout(title="Bond Price Composition")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📝 Step-by-Step Breakdown")

    cf_table = []
    cumulative_pv = 0
    for t in range(1, periods + 1):
        cf = coupon + (face if t == periods else 0)
        pv = cf / (1 + r) ** t
        cumulative_pv += pv
        cf_table.append({
            "Period": t,
            "Cash Flow (₹)": round(cf, 2),
            "Discount Factor": round(1 / (1 + r) ** t, 6),
            "PV (₹)": round(pv, 2),
            "Cumulative PV (₹)": round(cumulative_pv, 2)
        })

    df = pd.DataFrame(cf_table)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "📥 Download Cash Flow Table",
        df.to_csv(index=False),
        file_name="bond_cashflows.csv",
        mime="text/csv"
    )

# =========================================================
# YIELD TO MATURITY
# =========================================================

elif menu == "Yield to Maturity (YTM)":

    st.header("📊 Yield to Maturity (YTM)")

    st.markdown("""
## What is YTM?

YTM is the **single discount rate** that equates the present value of all bond cash flows
to its **current market price**.

It represents the **total annualised return** if:
- You hold the bond to maturity
- All coupons are reinvested at the YTM rate

---

## Approximation Formula

$$YTM \\approx \\frac{C + (F - P)/n}{(F + P)/2}$$

Where **C** = annual coupon, **F** = face value, **P** = current price, **n** = years to maturity
""")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        face = st.number_input("Face Value (₹)", value=1000.0, key="ytm_face")
    with col2:
        coupon_rate = st.number_input("Coupon Rate (%)", value=8.0, key="ytm_cr")
    with col3:
        n = int(st.number_input("Years to Maturity", value=5, min_value=1, step=1, key="ytm_n"))
    with col4:
        price = st.number_input("Current Market Price (₹)", value=950.0, key="ytm_p")

    annual_coupon = face * coupon_rate / 100

    # Approximation
    ytm_approx = (annual_coupon + (face - price) / n) / ((face + price) / 2) * 100

    # Exact YTM via numerical method (Newton-Raphson style using np)
    from scipy.optimize import brentq

    def bond_price(ytm, face, coupon, n):
        r = ytm / 100
        return sum([coupon / (1 + r) ** t for t in range(1, n + 1)]) + face / (1 + r) ** n

    try:
        ytm_exact = brentq(
            lambda y: bond_price(y, face, annual_coupon, n) - price,
            0.001, 99.999
        )
    except Exception:
        ytm_exact = ytm_approx / 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("YTM (Approximation Formula)", f"{round(ytm_approx, 4)}%")
    with col2:
        st.metric("YTM (Exact Calculation)", f"{round(ytm_exact, 4)}%")

    # Interpretation
    if price < face:
        st.success(f"Discount bond: YTM ({round(ytm_exact,2)}%) > Coupon Rate ({coupon_rate}%)")
    elif price > face:
        st.warning(f"Premium bond: YTM ({round(ytm_exact,2)}%) < Coupon Rate ({coupon_rate}%)")
    else:
        st.info(f"Par bond: YTM ({round(ytm_exact,2)}%) = Coupon Rate ({coupon_rate}%)")

    st.subheader("📘 Excel Formula")
    st.code('=RATE(nper, pmt, pv, fv) × frequency\nOR\n=YIELD(settlement, maturity, rate, pr, redemption, frequency)', language="excel")

    st.subheader("🧠 Key Relationships")

    key_rel = pd.DataFrame({
        "Condition": [
            "Price < Face Value",
            "Price = Face Value",
            "Price > Face Value"
        ],
        "Bond Type": ["Discount Bond", "Par Bond", "Premium Bond"],
        "YTM vs Coupon Rate": ["YTM > Coupon Rate", "YTM = Coupon Rate", "YTM < Coupon Rate"]
    })
    st.table(key_rel)

# =========================================================
# BOND PRICE-YIELD RELATIONSHIP
# =========================================================

elif menu == "Bond Price-Yield Relationship":

    st.header("📉 Bond Price-Yield Relationship")

    st.markdown("""
## The Fundamental Inverse Relationship

When **interest rates rise → Bond prices fall**

When **interest rates fall → Bond prices rise**

This is the most important relationship in fixed income investing.
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        face = st.number_input("Face Value (₹)", value=1000.0, key="pyr_face")
    with col2:
        coupon_rate = st.number_input("Coupon Rate (%)", value=8.0, key="pyr_cr")
    with col3:
        n = int(st.number_input("Years to Maturity", value=10, min_value=1, step=1, key="pyr_n"))

    annual_coupon = face * coupon_rate / 100

    ytm_range = np.arange(1, 20.1, 0.5)
    prices = []

    for ytm in ytm_range:
        r = ytm / 100
        p = sum([annual_coupon / (1 + r) ** t for t in range(1, n + 1)]) + face / (1 + r) ** n
        prices.append(p)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ytm_range,
        y=prices,
        mode='lines',
        name='Bond Price',
        line=dict(color='#185FA5', width=3)
    ))
    fig.add_hline(y=face, line_dash="dash", line_color="gray",
                  annotation_text="Par Value")
    fig.add_vline(x=coupon_rate, line_dash="dash", line_color="green",
                  annotation_text="Coupon Rate")

    fig.update_layout(
        title=f"Bond Price vs YTM ({coupon_rate}% coupon, {n} years)",
        xaxis_title="YTM (%)",
        yaxis_title="Bond Price (₹)",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔑 Key Observations")

    obs = [
        "The price-yield curve is convex (bowed toward origin) — prices fall less than they rise for equal YTM moves",
        f"At YTM = {coupon_rate}% (coupon rate), bond price = ₹{face:,.0f} (par)",
        "Longer maturity bonds have greater price sensitivity to yield changes",
        "Lower coupon bonds have greater price sensitivity than higher coupon bonds",
    ]
    for o in obs:
        st.markdown(f"- {o}")

    st.subheader("Malkiel's Bond Pricing Theorems")
    malkiel = pd.DataFrame({
        "Theorem": [
            "1. Price & Yield",
            "2. Maturity Effect",
            "3. Asymmetric Change",
            "4. Coupon Effect",
            "5. Price Sensitivity & Maturity",
        ],
        "Rule": [
            "Bond prices move inversely with yields",
            "Longer maturity → greater price sensitivity",
            "Price rise from yield fall > Price fall from equal yield rise",
            "Lower coupon → greater price sensitivity",
            "Price sensitivity increases at a diminishing rate with maturity",
        ]
    })
    st.table(malkiel)

# =========================================================
# DURATION & CONVEXITY
# =========================================================

elif menu == "Duration & Convexity":

    st.header("⏱️ Duration & Convexity")

    st.markdown("""
## What is Duration?

Duration measures the **price sensitivity** of a bond to changes in interest rates.

- **Macaulay Duration**: Weighted average time to receive cash flows (in years)
- **Modified Duration**: % change in price for 1% change in yield

$$\\text{Modified Duration} = \\frac{\\text{Macaulay Duration}}{1 + r}$$

$$\\Delta P \\approx -D_{mod} \\times \\Delta y \\times P$$
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        face = st.number_input("Face Value (₹)", value=1000.0, key="dur_face")
    with col2:
        coupon_rate = st.number_input("Coupon Rate (%)", value=8.0, key="dur_cr")
    with col3:
        n = int(st.number_input("Years to Maturity", value=5, min_value=1, step=1, key="dur_n"))

    ytm = st.number_input("YTM (%)", value=10.0, key="dur_ytm")

    r = ytm / 100
    coupon = face * coupon_rate / 100

    # Cash flows
    cash_flows = [coupon] * n
    cash_flows[-1] += face

    # Price
    price = sum([cf / (1 + r) ** t for t, cf in enumerate(cash_flows, 1)])

    # Macaulay Duration
    mac_dur = sum([t * (cf / (1 + r) ** t) / price for t, cf in enumerate(cash_flows, 1)])

    # Modified Duration
    mod_dur = mac_dur / (1 + r)

    # Convexity
    convexity = sum([t * (t + 1) * (cf / (1 + r) ** (t + 2)) for t, cf in enumerate(cash_flows, 1)]) / price

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Bond Price", currency(price))
    with col2:
        st.metric("Macaulay Duration", f"{round(mac_dur, 4)} years")
    with col3:
        st.metric("Modified Duration", f"{round(mod_dur, 4)}")
    with col4:
        st.metric("Convexity", f"{round(convexity, 4)}")

    # Price change estimation
    st.subheader("📐 Price Change Estimation")

    delta_y = st.slider("Change in Yield (%)", -3.0, 3.0, 1.0, step=0.25)

    dy = delta_y / 100
    price_change_duration = -mod_dur * dy * price
    price_change_convexity = 0.5 * convexity * (dy ** 2) * price
    total_price_change = price_change_duration + price_change_convexity
    new_price_approx = price + total_price_change

    # Actual new price
    ytm_new = (ytm + delta_y) / 100
    new_price_actual = sum([cf / (1 + ytm_new) ** t for t, cf in enumerate(cash_flows, 1)])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Duration-only estimate", currency(price - mod_dur * dy * price),
                  delta=f"{round(-mod_dur * dy * 100, 2)}%")
    with col2:
        st.metric("Duration + Convexity estimate", currency(new_price_approx),
                  delta=f"{round((new_price_approx/price - 1)*100, 2)}%")
    with col3:
        st.metric("Actual new price", currency(new_price_actual),
                  delta=f"{round((new_price_actual/price - 1)*100, 2)}%")

    st.info("""
Convexity correction improves the accuracy of duration-based price change estimates,
especially for large yield changes. Bonds with higher convexity are more valuable —
they gain more when yields fall and lose less when yields rise.
""")

# =========================================================
# TYPES OF BONDS
# =========================================================

elif menu == "Types of Bonds":

    st.header("🗂️ Types of Bonds")

    bond_types = pd.DataFrame({
        "Bond Type": [
            "Plain Vanilla (Bullet) Bond",
            "Zero Coupon Bond",
            "Floating Rate Bond (FRB)",
            "Government Security (G-Sec)",
            "Treasury Bill (T-Bill)",
            "Corporate Bond",
            "Convertible Bond",
            "Callable Bond",
            "Putable Bond",
            "Inflation-Indexed Bond (IIB)",
        ],
        "Key Feature": [
            "Fixed coupon + principal at maturity",
            "No coupon; issued at deep discount",
            "Coupon tied to benchmark rate (e.g. MIBOR)",
            "Issued by Central/State Govt; zero default risk",
            "Short-term (< 1 yr); issued at discount",
            "Issued by companies; carries credit risk",
            "Can be converted to equity at holder's option",
            "Issuer can redeem early (favours issuer)",
            "Holder can sell back early (favours investor)",
            "Principal/coupon adjusted for inflation (CPI)",
        ],
        "Indian Example": [
            "HDFC Ltd. 8.5% 2028 NCD",
            "REC Ltd. Zero Coupon 2025",
            "SBI FRB linked to MIBOR",
            "GoI 7.10% GS 2029",
            "91-day T-Bill",
            "Reliance Industries 6.95% 2027",
            "Tata Motors 0% Convertible 2025",
            "NTPC Callable Bond",
            "LIC Housing Finance Putable NCD",
            "GoI Inflation-Indexed Bond",
        ]
    })

    st.table(bond_types)

    st.subheader("Zero Coupon Bond Pricing")

    st.markdown("$$P = \\frac{F}{(1+r)^n}$$")

    col1, col2, col3 = st.columns(3)
    with col1:
        zcb_face = st.number_input("Face Value (₹)", value=1000.0, key="zcb_f")
    with col2:
        zcb_r = st.number_input("Required Return (%)", value=10.0, key="zcb_r")
    with col3:
        zcb_n = int(st.number_input("Years to Maturity", value=5, min_value=1, step=1, key="zcb_n"))

    zcb_price = zcb_face / (1 + zcb_r / 100) ** zcb_n
    zcb_discount = zcb_face - zcb_price

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"Zero Coupon Bond Price = {currency(zcb_price)}")
    with col2:
        st.info(f"Total Discount = {currency(zcb_discount)} ({round(zcb_discount/zcb_face*100,2)}%)")

# =========================================================
# STOCK BASICS & TERMINOLOGY
# =========================================================

elif menu == "Stock Basics & Terminology":

    st.header("📈 Stock Basics & Terminology")

    st.markdown("""
A **stock (equity share)** represents an ownership stake in a company.
Unlike bonds, stocks have **no fixed maturity** and **uncertain cash flows**.
""")

    terms = pd.DataFrame({
        "Term": [
            "Face Value (FV)",
            "Book Value per Share",
            "Market Price (CMP)",
            "Earnings per Share (EPS)",
            "Dividend per Share (DPS)",
            "Price-Earnings Ratio (P/E)",
            "Price-to-Book Ratio (P/B)",
            "Dividend Yield",
            "Payout Ratio",
            "Retention Ratio (b)",
            "Return on Equity (ROE)",
            "Sustainable Growth Rate (g)",
            "Required Return (Ke)",
            "Intrinsic Value",
        ],
        "Formula / Definition": [
            "Nominal value (₹2, ₹5, or ₹10 per share in India)",
            "Net Assets / Shares Outstanding",
            "Current traded price on NSE/BSE",
            "PAT / Shares Outstanding",
            "Total Dividends / Shares Outstanding",
            "Market Price / EPS",
            "Market Price / Book Value per Share",
            "DPS / Market Price × 100",
            "DPS / EPS × 100",
            "1 − Payout Ratio (fraction of earnings retained)",
            "PAT / Shareholders' Equity × 100",
            "ROE × Retention Ratio (b)",
            "Risk-free rate + Beta × Market Risk Premium",
            "Fair value based on fundamental analysis",
        ]
    })

    st.table(terms)

    st.subheader("📊 Intrinsic Value vs Market Price")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.error("**Overvalued**\nMarket Price > Intrinsic Value\nSell signal")
    with col2:
        st.info("**Fairly Valued**\nMarket Price ≈ Intrinsic Value\nHold")
    with col3:
        st.success("**Undervalued**\nMarket Price < Intrinsic Value\nBuy signal")

# =========================================================
# DIVIDEND DISCOUNT MODEL
# =========================================================

elif menu == "Dividend Discount Model (DDM)":

    st.header("💵 Dividend Discount Model (DDM)")

    st.markdown("""
## Core Concept

The value of a stock equals the **present value of all expected future dividends**.

$$P_0 = \\sum_{t=1}^{\\infty} \\frac{D_t}{(1+K_e)^t}$$

### Three Versions:
1. **Zero Growth DDM** — constant dividend forever
2. **Gordon Growth Model** — constant growth forever
3. **Multi-Stage DDM** — different growth phases
""")

    st.subheader("1. Zero Growth DDM (Perpetuity)")
    st.markdown("$$P_0 = \\frac{D}{K_e}$$")

    col1, col2 = st.columns(2)
    with col1:
        d_zero = st.number_input("Annual Dividend (₹)", value=50.0, key="ddm0_d")
    with col2:
        ke_zero = st.number_input("Required Return (%)", value=12.0, key="ddm0_k")

    if ke_zero > 0:
        p_zero = d_zero / (ke_zero / 100)
        st.success(f"Intrinsic Value = {currency(p_zero)}")

    st.markdown("---")
    st.subheader("2. Constant Growth DDM (Gordon Model)")
    st.markdown("$$P_0 = \\frac{D_1}{K_e - g}$$")

    col1, col2, col3 = st.columns(3)
    with col1:
        d1 = st.number_input("Next Year Dividend D₁ (₹)", value=20.0, key="ddm1_d")
    with col2:
        ke = st.number_input("Required Return Ke (%)", value=14.0, key="ddm1_k")
    with col3:
        g = st.number_input("Growth Rate g (%)", value=8.0, key="ddm1_g")

    if ke > g:
        p_gordon = d1 / ((ke - g) / 100)
        st.success(f"Intrinsic Value = {currency(p_gordon)}")
    else:
        st.error("Required return must be greater than growth rate (Ke > g)")

    st.markdown("---")
    st.subheader("3. Short-term Explicit Dividends")

    st.markdown("""
Value a stock with explicit dividends for 3 years, then sell at terminal price.
""")

    col1, col2 = st.columns(2)
    with col1:
        ke_exp = st.number_input("Required Return (%)", value=14.0, key="exp_ke")
        d_exp1 = st.number_input("Year 1 Dividend (₹)", value=10.0)
        d_exp2 = st.number_input("Year 2 Dividend (₹)", value=12.0)
        d_exp3 = st.number_input("Year 3 Dividend (₹)", value=14.0)
    with col2:
        g_terminal = st.number_input("Long-run Growth Rate (%)", value=7.0, key="exp_g")
        p3 = d_exp3 * (1 + g_terminal / 100) / ((ke_exp - g_terminal) / 100) if ke_exp > g_terminal else 0
        st.metric("Terminal Value at Year 3", currency(p3))

    if ke_exp > g_terminal:
        r = ke_exp / 100
        pv_divs = d_exp1/(1+r) + d_exp2/(1+r)**2 + d_exp3/(1+r)**3
        pv_terminal = p3 / (1+r)**3
        intrinsic = pv_divs + pv_terminal

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("PV of Dividends (Yrs 1-3)", currency(pv_divs))
        with col2:
            st.metric("PV of Terminal Value", currency(pv_terminal))
        with col3:
            st.metric("Intrinsic Value", currency(intrinsic))

# =========================================================
# GORDON GROWTH MODEL
# =========================================================

elif menu == "Gordon Growth Model":

    st.header("📊 Gordon Growth Model (GGM)")

    st.markdown("""
## Formula

$$P_0 = \\frac{D_1}{K_e - g} = \\frac{D_0(1+g)}{K_e - g}$$

## Growth Rate Estimation

$$g = ROE \\times b = ROE \\times (1 - \\text{Payout Ratio})$$
""")

    st.subheader("🔢 Interactive Calculator")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Option A: Enter D₁ directly**")
        d1_gg = st.number_input("D₁ — Next Year Dividend (₹)", value=25.0)
        ke_gg = st.number_input("Ke — Required Return (%)", value=15.0)
        g_gg = st.number_input("g — Growth Rate (%)", value=9.0)

    with col2:
        st.markdown("**Option B: Derive g from fundamentals**")
        roe = st.number_input("ROE (%)", value=18.0)
        payout = st.number_input("Payout Ratio (%)", value=40.0)
        b = 1 - payout / 100
        g_derived = roe * b
        st.metric("Derived Growth Rate (g = ROE × b)", f"{round(g_derived, 4)}%")
        st.caption(f"Retention ratio (b) = {round(b,4)}")

    if ke_gg > g_gg:
        p_gg = d1_gg / ((ke_gg - g_gg) / 100)
        st.success(f"**Intrinsic Value (using manual g) = {currency(p_gg)}**")

    if ke_gg > g_derived:
        p_gg_derived = d1_gg / ((ke_gg - g_derived) / 100)
        st.info(f"**Intrinsic Value (using derived g) = {currency(p_gg_derived)}**")
    elif ke_gg <= g_derived:
        st.error("⚠️ Derived growth rate ≥ Ke — model not applicable. Reduce ROE or increase payout.")

    # Sensitivity analysis
    st.subheader("📈 Sensitivity: Value vs Growth Rate")

    g_range = np.arange(0, ke_gg - 0.5, 0.5)
    values = [d1_gg / ((ke_gg - g) / 100) for g in g_range]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=g_range, y=values,
        mode='lines+markers',
        line=dict(color='#185FA5', width=2),
        name='Intrinsic Value'
    ))
    if ke_gg > g_gg:
        fig.add_vline(x=g_gg, line_dash="dash", line_color="green",
                      annotation_text=f"Current g={g_gg}%")
    fig.update_layout(
        title="Gordon Growth Model — Sensitivity to Growth Rate",
        xaxis_title="Growth Rate g (%)",
        yaxis_title="Intrinsic Value (₹)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.warning("""
⚠️ GGM Limitations:
- Assumes constant growth forever (unrealistic for high-growth firms)
- Very sensitive to small changes in Ke − g spread
- Not suitable for firms not paying dividends
- Growth rate must be < Ke (required return)
""")

# =========================================================
# MULTI-STAGE DDM
# =========================================================

elif menu == "Multi-Stage DDM":

    st.header("📈 Multi-Stage Dividend Discount Model")

    st.markdown("""
## Why Multi-Stage?

Most companies have **different growth phases**:

1. **High-growth phase** — startup / expansion (g₁ > normal)
2. **Transition phase** — growth slowing
3. **Stable phase** — mature company (g = sustainable)

**Two-Stage DDM Formula:**

$$P_0 = \\sum_{t=1}^{n} \\frac{D_0(1+g_1)^t}{(1+K_e)^t} + \\frac{P_n}{(1+K_e)^n}$$

Where $P_n = \\frac{D_{n+1}}{K_e - g_2}$
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        d0 = st.number_input("Current Dividend D₀ (₹)", value=10.0)
        ke_ms = st.number_input("Required Return Ke (%)", value=14.0, key="ms_ke")
    with col2:
        g1 = st.number_input("High Growth Rate g₁ (%)", value=20.0)
        n_high = int(st.number_input("High Growth Years", value=5, min_value=1, max_value=20, step=1))
    with col3:
        g2 = st.number_input("Stable Growth Rate g₂ (%)", value=7.0)

    if ke_ms > g2:
        r = ke_ms / 100

        # High growth phase dividends
        dividends = [d0 * (1 + g1 / 100) ** t for t in range(1, n_high + 1)]
        pv_divs = sum([d / (1 + r) ** t for t, d in enumerate(dividends, 1)])

        # Terminal value at end of high growth
        d_n1 = dividends[-1] * (1 + g2 / 100)
        p_n = d_n1 / ((ke_ms - g2) / 100)
        pv_terminal = p_n / (1 + r) ** n_high

        intrinsic = pv_divs + pv_terminal

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"PV of Dividends (Yrs 1-{n_high})", currency(pv_divs))
        with col2:
            st.metric("PV of Terminal Value", currency(pv_terminal))
        with col3:
            st.metric("Intrinsic Value", currency(intrinsic))

        # Dividend schedule
        div_table = []
        for t, d in enumerate(dividends, 1):
            pv = d / (1 + r) ** t
            div_table.append({"Year": t, "Phase": "High Growth", "Dividend (₹)": round(d, 2), "PV (₹)": round(pv, 2)})

        div_table.append({"Year": f"Terminal (at yr {n_high})", "Phase": "Stable",
                          "Dividend (₹)": round(d_n1, 2), "PV (₹)": round(pv_terminal, 2)})

        df_divs = pd.DataFrame(div_table)
        st.dataframe(df_divs, use_container_width=True)

        # Chart
        years_chart = list(range(1, n_high + 1))
        fig = go.Figure()
        fig.add_trace(go.Bar(x=years_chart, y=dividends,
                             name='Dividend', marker_color='#185FA5'))
        fig.update_layout(title="Dividend Growth Path",
                          xaxis_title="Year", yaxis_title="Dividend (₹)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Stable growth rate must be less than required return (g₂ < Ke)")

# =========================================================
# FCFE
# =========================================================

elif menu == "Free Cash Flow to Equity (FCFE)":

    st.header("💰 Free Cash Flow to Equity (FCFE) Valuation")

    st.markdown("""
## What is FCFE?

FCFE is the cash flow available to **equity shareholders** after:
- Operating expenses
- Interest payments
- Debt repayments
- Capital expenditures
- Working capital needs

$$FCFE = PAT + Depreciation - Capex - \\Delta Working\\ Capital + Net\\ Borrowings$$

$$P_0 = \\frac{FCFE_1}{K_e - g}$$  (if constant growth)
""")

    st.subheader("🔢 FCFE Calculator")

    col1, col2 = st.columns(2)

    with col1:
        pat = st.number_input("PAT / Net Income (₹ Cr)", value=500.0)
        depreciation = st.number_input("Depreciation (₹ Cr)", value=80.0)
        capex = st.number_input("Capital Expenditure (₹ Cr)", value=150.0)

    with col2:
        delta_wc = st.number_input("Increase in Working Capital (₹ Cr)", value=30.0)
        net_borrowings = st.number_input("Net New Borrowings (₹ Cr)", value=50.0)
        shares = st.number_input("Shares Outstanding (Cr)", value=100.0)

    fcfe_total = pat + depreciation - capex - delta_wc + net_borrowings
    fcfe_per_share = fcfe_total / shares if shares > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"Total FCFE = ₹{fcfe_total:,.2f} Cr")
    with col2:
        st.success(f"FCFE per Share = ₹{fcfe_per_share:,.2f}")

    st.subheader("📊 Intrinsic Value from FCFE")

    col1, col2 = st.columns(2)
    with col1:
        ke_fcfe = st.number_input("Required Return Ke (%)", value=14.0, key="fcfe_ke")
    with col2:
        g_fcfe = st.number_input("FCFE Growth Rate g (%)", value=9.0, key="fcfe_g")

    if ke_fcfe > g_fcfe and fcfe_per_share > 0:
        fcfe1 = fcfe_per_share * (1 + g_fcfe / 100)
        value_fcfe = fcfe1 / ((ke_fcfe - g_fcfe) / 100)
        st.success(f"**Intrinsic Value (FCFE model) = {currency(value_fcfe)} per share**")
    elif ke_fcfe <= g_fcfe:
        st.error("Required return must be > growth rate")

    st.info("""
**When to use FCFE vs DDM:**
- Use DDM when dividends are stable and reflect earning capacity
- Use FCFE when dividends don't reflect true earning power (low payout firms)
- FCFE is more appropriate for firms in India that retain most earnings
""")

# =========================================================
# PRICE MULTIPLES
# =========================================================

elif menu == "Price Multiples & Relative Valuation":

    st.header("📊 Price Multiples & Relative Valuation")

    st.markdown("""
Relative valuation compares a stock's multiples to:
- Industry peers
- Historical averages
- Benchmark index

Key multiples used in Indian equity research:
""")

    st.subheader("1. P/E Ratio Valuation")

    col1, col2, col3 = st.columns(3)
    with col1:
        eps = st.number_input("EPS (₹)", value=50.0)
    with col2:
        pe_justified = st.number_input("Justified P/E (Industry/Peer)", value=20.0)
    with col3:
        cmp = st.number_input("Current Market Price (₹)", value=900.0)

    intrinsic_pe = eps * pe_justified
    actual_pe = cmp / eps if eps > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Intrinsic Value (P/E)", currency(intrinsic_pe))
    with col2:
        st.metric("Actual P/E", round(actual_pe, 2))
    with col3:
        st.metric("Justified P/E", pe_justified)

    if intrinsic_pe > cmp:
        st.success(f"**UNDERVALUED** — Intrinsic ({currency(intrinsic_pe)}) > Market ({currency(cmp)})")
    else:
        st.warning(f"**OVERVALUED** — Intrinsic ({currency(intrinsic_pe)}) < Market ({currency(cmp)})")

    st.subheader("2. P/B Ratio Valuation")

    col1, col2 = st.columns(2)
    with col1:
        bvps = st.number_input("Book Value per Share (₹)", value=200.0)
        pb_justified = st.number_input("Justified P/B (Industry)", value=3.5)
    with col2:
        intrinsic_pb = bvps * pb_justified
        actual_pb = cmp / bvps if bvps > 0 else 0
        st.metric("Intrinsic Value (P/B)", currency(intrinsic_pb))
        st.metric("Actual P/B", round(actual_pb, 2))

    st.subheader("3. EV/EBITDA Multiple")

    col1, col2, col3 = st.columns(3)
    with col1:
        ebitda = st.number_input("EBITDA (₹ Cr)", value=1000.0)
        ev_ebitda_peer = st.number_input("Peer EV/EBITDA", value=12.0)
    with col2:
        debt = st.number_input("Total Debt (₹ Cr)", value=500.0)
        cash = st.number_input("Cash & Equivalents (₹ Cr)", value=200.0)
    with col3:
        shares_ev = st.number_input("Shares Outstanding (Cr)", value=100.0, key="ev_shares")

    ev_implied = ebitda * ev_ebitda_peer
    equity_value = ev_implied - debt + cash
    value_per_share = equity_value / shares_ev if shares_ev > 0 else 0

    st.success(f"Implied EV = ₹{ev_implied:,.2f} Cr | Equity Value = ₹{equity_value:,.2f} Cr | Per Share = {currency(value_per_share)}")

    st.subheader("📋 Multiples Comparison Table")

    multiples_df = pd.DataFrame({
        "Multiple": ["P/E", "P/B", "EV/EBITDA", "Dividend Yield", "PEG Ratio"],
        "Formula": ["Price/EPS", "Price/BVPS", "EV/EBITDA", "DPS/Price", "P/E ÷ EPS Growth Rate"],
        "Good for": [
            "Mature, profitable companies",
            "Asset-heavy industries (banks, realty)",
            "Cross-border/sector comparison",
            "Income-seeking investors",
            "Growth-adjusted valuation"
        ],
        "Limitation": [
            "Affected by accounting choices",
            "Ignores intangibles",
            "Varies by capital structure",
            "Low for high-growth firms",
            "Sensitive to growth estimate"
        ]
    })
    st.table(multiples_df)

# =========================================================
# CAPM
# =========================================================

elif menu == "CAPM & Required Return":

    st.header("📐 CAPM & Required Return on Equity")

    st.markdown("""
## Capital Asset Pricing Model (CAPM)

$$K_e = R_f + \\beta \\times (R_m - R_f)$$

Where:
- **Ke** = Required return on equity
- **Rf** = Risk-free rate (10-yr G-Sec yield)
- **β (Beta)** = Systematic risk of the stock
- **(Rm − Rf)** = Equity Risk Premium (ERP)
""")

    col1, col2, col3 = st.columns(3)
    with col1:
        rf = st.number_input("Risk-Free Rate Rf (%)\n(10-yr G-Sec)", value=7.0)
    with col2:
        beta = st.number_input("Beta (β)", value=1.2, min_value=0.0, max_value=5.0, step=0.1)
    with col3:
        erp = st.number_input("Equity Risk Premium\n(Rm − Rf) (%)", value=6.0)

    ke = rf + beta * erp

    st.success(f"**Required Return (Ke) = {round(ke, 4)}%**")
    st.latex(f"K_e = {rf}\\% + {beta} \\times {erp}\\% = {round(ke,2)}\\%")

    # Beta interpretation
    st.subheader("📊 Beta Interpretation")

    beta_table = pd.DataFrame({
        "Beta": ["β = 0", "0 < β < 1", "β = 1", "β > 1", "β < 0"],
        "Interpretation": [
            "No systematic risk (e.g. cash)",
            "Less volatile than market (e.g. FMCG, pharma)",
            "Moves with market",
            "More volatile than market (e.g. banks, metals, IT)",
            "Moves opposite to market (rare)"
        ],
        "Examples (India)": [
            "T-Bills / G-Secs",
            "HUL, Nestle, Sun Pharma",
            "Diversified large-cap fund",
            "Adani Ports, Tata Steel, Infosys",
            "Some hedge fund strategies"
        ]
    })
    st.table(beta_table)

    # SML
    st.subheader("Security Market Line (SML)")

    beta_range = np.arange(0, 2.5, 0.1)
    ke_range = rf + beta_range * erp

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=beta_range, y=ke_range,
        mode='lines', name='SML',
        line=dict(color='#185FA5', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=[beta], y=[ke],
        mode='markers', name=f'Your Stock (β={beta})',
        marker=dict(size=12, color='red')
    ))
    fig.update_layout(
        title="Security Market Line",
        xaxis_title="Beta (β)",
        yaxis_title="Required Return (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# RISK PREMIUM & BETA
# =========================================================

elif menu == "Risk Premium & Beta":

    st.header("⚡ Risk Premium & Beta Analysis")

    st.markdown("""
## Risk Decomposition

**Total Risk = Systematic Risk + Unsystematic Risk**

| Type | Also Called | Diversifiable? | Measured By |
|---|---|---|---|
| Systematic | Market risk | ❌ No | Beta (β) |
| Unsystematic | Firm-specific | ✅ Yes | Standard deviation beyond β |

Only **systematic risk** is compensated in CAPM.
""")

    st.subheader("Beta Calculation from Returns")

    st.markdown("Upload or simulate stock and market returns to estimate beta.")

    if st.checkbox("Use Simulated Data"):
        np.random.seed(42)
        market_ret = np.random.normal(0.01, 0.04, 60)
        true_beta = st.slider("True Beta (for simulation)", 0.5, 2.5, 1.3, step=0.1)
        alpha = 0.002
        stock_ret = alpha + true_beta * market_ret + np.random.normal(0, 0.02, 60)

        slope, intercept, r_value, p_value, std_err = stats.linregress(market_ret, stock_ret)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Estimated Beta", round(slope, 4))
        with col2:
            st.metric("Alpha (Jensen's)", round(intercept * 100, 4))
        with col3:
            st.metric("R² (Coefficient of Determination)", round(r_value**2, 4))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=market_ret * 100, y=stock_ret * 100,
            mode='markers', name='Observations',
            marker=dict(size=6, color='#185FA5', opacity=0.6)
        ))
        # Regression line
        x_line = np.linspace(min(market_ret), max(market_ret), 100)
        y_line = intercept + slope * x_line
        fig.add_trace(go.Scatter(
            x=x_line * 100, y=y_line * 100,
            mode='lines', name=f'Regression (β={round(slope,2)})',
            line=dict(color='red', width=2)
        ))
        fig.update_layout(
            title="Characteristic Line (Stock vs Market Returns)",
            xaxis_title="Market Return (%)",
            yaxis_title="Stock Return (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# VALUATION DECISION TOOL
# =========================================================

elif menu == "Valuation Decision Tool":

    st.header("🧮 Valuation Model Selection Tool")

    st.markdown("Answer a few questions to get the recommended valuation model.")

    asset_type = st.radio("What are you valuing?", ["Stock (Equity)", "Bond (Fixed Income)"])

    if asset_type == "Bond (Fixed Income)":
        known = st.radio("What do you know?", ["Current price — find YTM", "Required return — find price"])
        if known == "Required return — find price":
            st.success("**Recommended: Bond Valuation Module** → Go to 'Bond Valuation'")
        else:
            st.success("**Recommended: YTM Calculator** → Go to 'Yield to Maturity (YTM)'")

    else:
        pays_div = st.radio("Does the company pay dividends?", ["Yes", "No / Irregular"])

        if pays_div == "Yes":
            growth_type = st.radio("What is the dividend growth pattern?",
                                   ["Zero growth (fixed dividend)",
                                    "Constant growth",
                                    "High growth then stable (two-stage)"])

            if growth_type == "Zero growth (fixed dividend)":
                st.success("**Recommended: Zero Growth DDM** → P₀ = D/Ke")
            elif growth_type == "Constant growth":
                st.success("**Recommended: Gordon Growth Model** → P₀ = D₁/(Ke − g)")
            else:
                st.success("**Recommended: Multi-Stage DDM** → Go to 'Multi-Stage DDM'")

        else:
            fcfe_avail = st.radio("Is FCFE positive and forecastable?", ["Yes", "No"])

            if fcfe_avail == "Yes":
                st.success("**Recommended: FCFE Valuation** → Go to 'Free Cash Flow to Equity'")
            else:
                st.success("**Recommended: Price Multiples (P/E, EV/EBITDA)** → Relative Valuation")

    st.subheader("📋 Quick Reference: When to Use Which Model")

    guide = pd.DataFrame({
        "Model": ["Zero-Growth DDM", "Gordon Growth Model", "Multi-Stage DDM",
                  "FCFE", "P/E Multiple", "EV/EBITDA", "Bond Valuation", "YTM"],
        "Best For": [
            "Preferred shares, REITs",
            "Mature stable companies (FMCG, utilities)",
            "IT, pharma in growth phase",
            "Companies with low/no dividend payout",
            "Profitable companies, peer comparison",
            "Capital-intensive, leveraged firms",
            "Finding fair price given YTM",
            "Finding return given market price"
        ]
    })
    st.table(guide)

# =========================================================
# STEP-BY-STEP SOLVER
# =========================================================

elif menu == "Step-by-Step Solver":

    st.header("🧠 Step-by-Step Solver")

    problem = st.selectbox(
        "Choose Problem",
        [
            "Bond Valuation",
            "Yield to Maturity (Approximation)",
            "Gordon Growth Model",
            "CAPM Required Return",
            "Multi-Stage DDM",
        ]
    )

    if problem == "Bond Valuation":

        face = st.number_input("Face Value (₹)", value=1000.0)
        cr = st.number_input("Coupon Rate (%)", value=8.0)
        n = int(st.number_input("Years", value=5, min_value=1, step=1))
        ytm = st.number_input("YTM / Required Return (%)", value=10.0)

        coupon = face * cr / 100
        r = ytm / 100

        st.write("**Step 1: Identify coupon payment**")
        st.latex(f"C = {face} \\times {cr/100} = {coupon}")

        st.write("**Step 2: Identify formula**")
        st.latex(r"P = \sum_{t=1}^{n} \frac{C}{(1+r)^t} + \frac{F}{(1+r)^n}")

        st.write("**Step 3: Calculate PV of coupons**")
        pv_c = coupon * (1 - (1+r)**(-n)) / r
        st.latex(f"PV_{{coupons}} = {coupon} \\times \\frac{{1-(1.{int(ytm)})^{{-{n}}}}}{{{r}}} = {round(pv_c,2)}")

        st.write("**Step 4: Calculate PV of face value**")
        pv_f = face / (1+r)**n
        st.latex(f"PV_{{face}} = \\frac{{{face}}}{{(1+{r})^{{{n}}}}} = {round(pv_f,2)}")

        st.write("**Step 5: Add to get price**")
        price = pv_c + pv_f
        st.success(f"P = {round(pv_c,2)} + {round(pv_f,2)} = **{currency(price)}**")

    elif problem == "Yield to Maturity (Approximation)":
        face = st.number_input("Face Value (₹)", value=1000.0, key="ytm_sbs_f")
        cr = st.number_input("Coupon Rate (%)", value=8.0, key="ytm_sbs_cr")
        n = int(st.number_input("Years", value=5, min_value=1, step=1, key="ytm_sbs_n"))
        price = st.number_input("Current Price (₹)", value=950.0, key="ytm_sbs_p")

        coupon = face * cr / 100

        st.write("**Step 1: Identify approximation formula**")
        st.latex(r"YTM \approx \frac{C + (F-P)/n}{(F+P)/2}")

        st.write("**Step 2: Substitute values**")
        numerator = coupon + (face - price) / n
        denominator = (face + price) / 2
        st.latex(f"YTM = \\frac{{{coupon} + ({face}-{price})/{n}}}{{{denominator}}}")

        ytm_approx = numerator / denominator * 100
        st.write("**Step 3: Calculate**")
        st.success(f"YTM ≈ {round(ytm_approx, 4)}%")

    elif problem == "Gordon Growth Model":
        d1 = st.number_input("D₁ — Next Year Dividend (₹)", value=20.0, key="ggm_sbs_d1")
        ke = st.number_input("Ke — Required Return (%)", value=14.0, key="ggm_sbs_ke")
        g = st.number_input("g — Growth Rate (%)", value=8.0, key="ggm_sbs_g")

        st.write("**Step 1: Identify formula**")
        st.latex(r"P_0 = \frac{D_1}{K_e - g}")

        st.write("**Step 2: Verify Ke > g**")
        if ke > g:
            st.success(f"✅ {ke}% > {g}% — Model is valid")
        else:
            st.error("❌ Ke ≤ g — model undefined")
            st.stop()

        st.write("**Step 3: Calculate**")
        p0 = d1 / ((ke - g) / 100)
        st.latex(f"P_0 = \\frac{{{d1}}}{{{ke/100} - {g/100}}} = \\frac{{{d1}}}{{{(ke-g)/100}}}")
        st.success(f"P₀ = **{currency(p0)}**")

    elif problem == "CAPM Required Return":
        rf = st.number_input("Risk-Free Rate (%)", value=7.0, key="capm_sbs_rf")
        beta = st.number_input("Beta (β)", value=1.2, key="capm_sbs_b")
        erp = st.number_input("Equity Risk Premium (%)", value=6.0, key="capm_sbs_erp")

        st.write("**Step 1: Identify formula**")
        st.latex(r"K_e = R_f + \beta \times (R_m - R_f)")

        st.write("**Step 2: Substitute values**")
        ke = rf + beta * erp
        st.latex(f"K_e = {rf} + {beta} \\times {erp}")

        st.write("**Step 3: Calculate**")
        st.success(f"Ke = {round(ke, 4)}%")

    elif problem == "Multi-Stage DDM":
        d0 = st.number_input("Current Dividend D₀ (₹)", value=10.0, key="ms_sbs_d0")
        g1 = st.number_input("High Growth Rate (%)", value=20.0, key="ms_sbs_g1")
        n_h = int(st.number_input("High Growth Years", value=3, min_value=1, step=1, key="ms_sbs_n"))
        g2 = st.number_input("Stable Growth Rate (%)", value=7.0, key="ms_sbs_g2")
        ke = st.number_input("Required Return Ke (%)", value=14.0, key="ms_sbs_ke")

        if ke > g2:
            r = ke / 100
            st.write("**Step 1: Calculate high-growth dividends**")
            divs = [d0 * (1 + g1/100)**t for t in range(1, n_h+1)]
            for t, d in enumerate(divs, 1):
                st.latex(f"D_{t} = {d0}(1+{g1/100})^{t} = {round(d,2)}")

            st.write("**Step 2: Calculate terminal value**")
            d_n1 = divs[-1] * (1 + g2/100)
            p_n = d_n1 / ((ke - g2)/100)
            st.latex(f"P_{n_h} = \\frac{{{round(d_n1,2)}}}{{{ke/100}-{g2/100}}} = {round(p_n,2)}")

            st.write("**Step 3: Discount all to today**")
            pv_d = sum([d/(1+r)**t for t, d in enumerate(divs, 1)])
            pv_p = p_n / (1+r)**n_h
            p0 = pv_d + pv_p
            st.success(f"P₀ = {round(pv_d,2)} + {round(pv_p,2)} = **{currency(p0)}**")

# =========================================================
# AI HINT SYSTEM
# =========================================================

elif menu == "AI Hint System":

    st.header("🤖 AI Hint System — Bond & Stock Valuation")

    problems = {
        "Bond Valuation": {
            "question": "A bond has face value ₹1,000, coupon rate 9%, maturity 4 years. Required return = 11%. Find the bond price.",
            "correct": sum([90/(1.11)**t for t in range(1,5)]) + 1000/(1.11)**4,
            "hints": [
                "Is the YTM > coupon rate? What does that tell you about the price?",
                "Split into two parts: PV of coupon annuity + PV of face value",
                "PV of coupons = C × [(1-(1+r)^-n)/r] = 90 × [(1-1.11^-4)/0.11]",
            ],
            "formula": r"P = 90 \times \frac{1-1.11^{-4}}{0.11} + \frac{1000}{1.11^4}"
        },
        "Gordon Growth Model": {
            "question": "A stock pays D₀ = ₹15, g = 10%, Ke = 16%. Find intrinsic value.",
            "correct": 15 * 1.10 / (0.16 - 0.10),
            "hints": [
                "You are given D₀, not D₁. First find D₁ = D₀ × (1+g)",
                "GGM formula: P₀ = D₁ / (Ke - g)",
                f"D₁ = 15 × 1.10 = 16.5. Then P₀ = 16.5 / (0.16-0.10)",
            ],
            "formula": r"P_0 = \frac{D_0(1+g)}{K_e - g} = \frac{15 \times 1.10}{0.16 - 0.10}"
        },
        "YTM Approximation": {
            "question": "Bond: Face ₹1,000, Coupon 7%, 5 years, Price ₹940. Find approximate YTM.",
            "correct": (70 + (1000-940)/5) / ((1000+940)/2) * 100,
            "hints": [
                "YTM approx = [C + (F-P)/n] / [(F+P)/2]",
                "Annual coupon C = 1000 × 7% = ₹70",
                "Numerator = 70 + (1000-940)/5 = 70 + 12 = 82; Denominator = (1000+940)/2 = 970",
            ],
            "formula": r"YTM \approx \frac{70 + (1000-940)/5}{(1000+940)/2}"
        }
    }

    selected = st.selectbox("Choose Problem", list(problems.keys()))
    prob = problems[selected]

    st.markdown(f"**Problem:** {prob['question']}")

    answer = st.number_input("Enter Your Answer (₹ or %)", value=0.0)

    if st.button("Check Answer"):
        if abs(answer - prob['correct']) < 1.0:
            st.success(f"✅ Correct! Answer = {round(prob['correct'], 2)}")
            st.balloons()
        else:
            st.error(f"❌ Incorrect. You're off by {round(abs(answer-prob['correct']),2)}. Use hints below.")

    for i, hint in enumerate(prob['hints'], 1):
        if st.checkbox(f"Hint {i}"):
            st.info(f"💡 {hint}")

    if st.checkbox("Show Full Solution"):
        st.latex(prob['formula'])
        st.success(f"Correct Answer = {round(prob['correct'], 4)}")

# =========================================================
# QUIZ ENGINE
# =========================================================

elif menu == "Quiz Engine":

    st.header("📝 Valuation Quiz Engine")

    difficulty = st.selectbox("Choose Difficulty", ["Beginner", "Intermediate", "Advanced"])

    if "val_quiz_generated" not in st.session_state or st.button("🔄 New Question"):
        if difficulty == "Beginner":
            # Bond price question
            st.session_state.q_face = random.choice([1000, 500])
            st.session_state.q_cr = random.choice([7, 8, 9, 10])
            st.session_state.q_n = random.choice([3, 4, 5])
            st.session_state.q_ytm = random.choice([8, 10, 12])
            st.session_state.q_type = "bond"
        elif difficulty == "Intermediate":
            st.session_state.q_d1 = random.choice([15, 20, 25, 30])
            st.session_state.q_ke = random.choice([12, 14, 15, 16])
            st.session_state.q_g = random.choice([5, 6, 7, 8, 9])
            st.session_state.q_type = "ggm"
        else:
            st.session_state.q_rf = random.choice([6, 7, 7.5])
            st.session_state.q_beta = random.choice([0.8, 1.0, 1.2, 1.5])
            st.session_state.q_erp = random.choice([5, 6, 7])
            st.session_state.q_type = "capm"
        st.session_state.val_quiz_generated = True

    qtype = st.session_state.q_type

    if qtype == "bond":
        face = st.session_state.q_face
        cr = st.session_state.q_cr
        n = st.session_state.q_n
        ytm = st.session_state.q_ytm
        r = ytm / 100
        coupon = face * cr / 100
        correct = coupon * (1-(1+r)**(-n))/r + face/(1+r)**n

        st.markdown(f"""
**Calculate the bond price:**

- Face Value = ₹{face}
- Coupon Rate = {cr}%
- Years to Maturity = {n}
- Required Return = {ytm}%
""")

    elif qtype == "ggm":
        d1 = st.session_state.q_d1
        ke = st.session_state.q_ke
        g = st.session_state.q_g
        if ke > g:
            correct = d1 / ((ke - g) / 100)
        else:
            correct = 0

        st.markdown(f"""
**Find intrinsic value using Gordon Growth Model:**

- D₁ (next dividend) = ₹{d1}
- Required Return Ke = {ke}%
- Growth Rate g = {g}%
""")

    else:
        rf = st.session_state.q_rf
        beta = st.session_state.q_beta
        erp = st.session_state.q_erp
        correct = rf + beta * erp

        st.markdown(f"""
**Find the required return using CAPM:**

- Risk-free Rate = {rf}%
- Beta = {beta}
- Equity Risk Premium = {erp}%
""")

    ans = st.number_input("Your Answer", value=0.0, key="val_quiz_ans")

    if st.button("Submit Answer"):
        if abs(ans - correct) < 1.0:
            st.success(f"✅ Correct! Answer = {round(correct, 2)}")
            st.balloons()
        else:
            st.error(f"❌ Incorrect. Correct = {round(correct, 2)}")

# =========================================================
# EXCEL FORMULA TRAINER
# =========================================================

elif menu == "Excel Formula Trainer":

    st.header("📊 Excel Formula Trainer — Valuation")

    problems = {
        "Bond Price (Annual)": {
            "desc": "Price a bond: FV=₹1000, Coupon=8%, n=5, YTM=10%",
            "fn": "PV",
            "answer": "=PV(10%,5,-80,-1000)",
            "hint": "PV(rate, nper, pmt, [fv]) — note negative signs for cash outflows"
        },
        "Bond Price (Semi-Annual)": {
            "desc": "Semi-annual bond: FV=₹1000, Coupon=8%, 5yr, YTM=10%",
            "fn": "PV",
            "answer": "=PV(10%/2, 5*2, -40, -1000)",
            "hint": "Divide rate by 2, multiply periods by 2 for semi-annual"
        },
        "YTM": {
            "desc": "Find YTM: FV=₹1000, Coupon=₹80/yr, 5yr, Price=₹950",
            "fn": "RATE",
            "answer": "=RATE(5,-80,950,-1000)*1",
            "hint": "RATE(nper, pmt, pv, [fv]) — price is positive PV, coupon is negative PMT"
        },
        "Duration": {
            "desc": "Find Macaulay Duration — use DURATION() function",
            "fn": "DURATION",
            "answer": "=DURATION(settlement, maturity, coupon, yield, frequency)",
            "hint": "DURATION(settlement, maturity, coupon_rate, yield, freq, [basis])"
        },
        "Intrinsic Value (GGM)": {
            "desc": "GGM: D₁=₹20, Ke=14%, g=8%",
            "fn": "=",
            "answer": "=20/(14%-8%)",
            "hint": "Direct formula — no built-in function. P₀ = D₁ / (Ke - g)"
        }
    }

    sel = st.selectbox("Choose Problem", list(problems.keys()))
    prob = problems[sel]

    st.subheader("Problem")
    st.markdown(prob["desc"])
    st.info(f"💡 Function hint: `{prob['hint']}`")

    user_inp = st.text_input("Enter Excel Formula (start with =)")

    if st.button("Validate"):
        if prob["fn"].upper() in user_inp.upper() or user_inp.strip().startswith("="):
            st.success(f"✅ Correct function! Reference answer: `{prob['answer']}`")
        else:
            st.error(f"❌ Try using the {prob['fn']}() function or a direct formula.")

    if st.checkbox("Show Answer"):
        st.code(prob["answer"], language="excel")

# =========================================================
# FORMULA CHEAT SHEET
# =========================================================

elif menu == "Formula Cheat Sheet":

    st.header("📘 Stock & Bond Valuation Formula Cheat Sheet")

    formulas = """
STOCK & BOND VALUATION FORMULAS
==================================================

──────────────────────────────────────────────────
BOND VALUATION
──────────────────────────────────────────────────
1. Bond Price
   P = Σ[C/(1+r)^t] + F/(1+r)^n
   Excel: =PV(ytm, n, -coupon, -face)

2. Zero Coupon Bond Price
   P = F / (1+r)^n

3. YTM Approximation
   YTM ≈ [C + (F-P)/n] / [(F+P)/2]
   Excel: =RATE(n, -coupon, price, -face)

4. Current Yield
   Current Yield = Annual Coupon / Market Price

5. Macaulay Duration
   D_mac = Σ[t × PV(CF_t)] / P
   Excel: =DURATION(settlement, maturity, cr, ytm, freq)

6. Modified Duration
   D_mod = D_mac / (1+r)

7. Price Change (Duration)
   ΔP ≈ −D_mod × Δy × P

8. Price Change (Duration + Convexity)
   ΔP ≈ (−D_mod × Δy + 0.5 × Convexity × Δy²) × P

──────────────────────────────────────────────────
STOCK VALUATION — DDM
──────────────────────────────────────────────────
9. Zero Growth DDM
   P₀ = D / Ke

10. Gordon Growth Model (Constant Growth)
    P₀ = D₁ / (Ke − g)
    P₀ = D₀(1+g) / (Ke − g)
    Requires: Ke > g

11. Growth Rate (Sustainable)
    g = ROE × b = ROE × (1 − Payout Ratio)

12. Multi-Stage DDM
    P₀ = Σ[D_t/(1+Ke)^t] + P_n/(1+Ke)^n
    P_n = D_(n+1) / (Ke − g_stable)

──────────────────────────────────────────────────
STOCK VALUATION — FCFE
──────────────────────────────────────────────────
13. FCFE Calculation
    FCFE = PAT + Depreciation − Capex − ΔNWC + Net Borrowings

14. FCFE Value
    P₀ = FCFE₁ / (Ke − g)

──────────────────────────────────────────────────
PRICE MULTIPLES
──────────────────────────────────────────────────
15. P/E Ratio
    P/E = Market Price / EPS
    Intrinsic = EPS × Justified P/E

16. P/B Ratio
    P/B = Market Price / Book Value per Share

17. EV/EBITDA
    EV = Market Cap + Debt − Cash
    EV/EBITDA Multiple used for cross-firm comparison

18. Dividend Yield
    DY = DPS / Market Price × 100

19. PEG Ratio
    PEG = P/E / Earnings Growth Rate
    PEG < 1 suggests undervaluation

──────────────────────────────────────────────────
REQUIRED RETURN
──────────────────────────────────────────────────
20. CAPM
    Ke = Rf + β × (Rm − Rf)
    Ke = Rf + β × ERP

21. Dividend Growth Model (Ke)
    Ke = D₁/P₀ + g

──────────────────────────────────────────────────
BOND PRICING RULES (Malkiel)
──────────────────────────────────────────────────
- YTM > Coupon Rate → Discount Bond (P < Face)
- YTM < Coupon Rate → Premium Bond (P > Face)
- YTM = Coupon Rate → Par Bond (P = Face)
- At maturity, price always → Face Value

──────────────────────────────────────────────────
COMMON MISTAKES
──────────────────────────────────────────────────
- Forgetting D₁ = D₀(1+g) in Gordon Growth Model
- Using annual YTM instead of semi-annual for semi-annual bonds
- Excel NPV: =PV() for bonds (not NPV function)
- Confusing current yield with YTM
- Ignoring the sign convention in Excel PV()
- Applying GGM when g ≥ Ke
──────────────────────────────────────────────────
"""

    st.text_area("Formula Reference", formulas, height=800)

    st.download_button(
        label="📥 Download Formula Cheat Sheet",
        data=formulas,
        file_name="Stock_Bond_Valuation_Formulas.txt"
    )

# =========================================================
# COMMON STUDENT MISTAKES
# =========================================================

elif menu == "Common Student Mistakes":

    st.header("⚠️ Common Student Mistakes in Valuation")

    mistakes = pd.DataFrame({
        "Mistake": [
            "Using D₀ instead of D₁ in GGM",
            "Semi-annual bonds: using annual rate/periods",
            "Confusing Current Yield with YTM",
            "Using Excel NPV() for bond pricing",
            "Ignoring sign convention in Excel PV()",
            "Applying GGM when g ≥ Ke",
            "Confusing Macaulay and Modified Duration",
            "Forgetting to multiply Beta × ERP in CAPM",
            "Using book value beta instead of levered beta",
            "Treating P/E as universal valuation tool",
            "Forgetting terminal value in multi-stage DDM",
            "Discounting FCFE at WACC instead of Ke",
        ],
        "Explanation": [
            "GGM uses D₁ (next year dividend). If given D₀: D₁ = D₀ × (1+g)",
            "Semi-annual: rate = YTM/2, periods = n×2, coupon = annual coupon/2",
            "Current yield = coupon/price. YTM includes capital gain/loss to maturity",
            "Use =PV(ytm, n, -coupon, -face) for bond pricing, not NPV()",
            "In =PV(), coupon is negative (outflow from issuer's view). Price is positive",
            "GGM denominator (Ke − g) must be positive. Model breaks if g ≥ Ke",
            "Duration (Macaulay) measures time. Modified duration = Mac. duration/(1+r) measures price sensitivity",
            "CAPM: Ke = Rf + β×ERP. Students often write Ke = Rf + β only",
            "Use market-based beta from regression, not accounting ratios",
            "P/E invalid for loss-making firms, cyclical industries, or cross-country comparison",
            "Value = PV of explicit dividends + PV of terminal value. Both must be included",
            "FCFE is equity cash flow → discount at Ke. FCFF is for all investors → discount at WACC",
        ]
    })

    st.table(mistakes)

    st.warning("""
**Top 3 Exam Mistakes to Avoid:**

1. **D₀ vs D₁** — always check which is given. Multiply by (1+g) if D₀ is given.
2. **Semi-annual compounding** — divide rate by 2, multiply periods by 2.
3. **GGM requires Ke > g** — always verify before applying.
""")

# =========================================================
# ADVANCED QUIZ BANK
# =========================================================

elif menu == "Advanced Quiz Bank":

    st.header("📝 Advanced Quiz Bank — Valuation")

    level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])

    if level == "Beginner":
        st.markdown("""
**Problem:** A bond has face value ₹1,000, coupon rate 10%, 3-year maturity.
Required return = 12%. Find the bond price.
""")
        r = 0.12
        coupon = 100
        face = 1000
        correct = sum([coupon/(1.12)**t for t in range(1,4)]) + 1000/(1.12)**3

        ans = st.number_input("Your Answer (₹)", value=0.0, key="aqb_beg")
        if st.button("Evaluate", key="aqb_beg_btn"):
            if abs(ans - correct) < 1:
                st.success(f"✅ Correct! Price = {currency(correct)}")
                st.balloons()
            else:
                st.error(f"❌ Correct Answer = {currency(correct)}")
                st.info("Discount bond: YTM (12%) > Coupon (10%), so Price < ₹1,000")

    elif level == "Intermediate":
        st.markdown("""
**Problem:** Infosys current dividend D₀ = ₹30. Dividends expected to grow at 12%
for 3 years, then stabilise at 7% forever. Required return = 15%.

Find intrinsic value.
""")
        ke = 0.15; g1 = 0.12; g2 = 0.07; d0 = 30
        divs = [d0*(1.12)**t for t in range(1,4)]
        pv_d = sum([d/(1.15)**t for t,d in enumerate(divs,1)])
        d4 = divs[-1]*(1.07)
        p3 = d4/(0.15-0.07)
        pv_p = p3/(1.15)**3
        correct = pv_d + pv_p

        ans = st.number_input("Your Answer (₹)", value=0.0, key="aqb_int")
        if st.button("Evaluate", key="aqb_int_btn"):
            if abs(ans - correct) < 2:
                st.success(f"✅ Correct! Intrinsic Value = {currency(correct)}")
                st.balloons()
            else:
                st.error(f"❌ Correct Answer = {currency(correct)}")
                st.markdown(f"""
**Solution breakdown:**
- D₁={round(divs[0],2)}, D₂={round(divs[1],2)}, D₃={round(divs[2],2)}
- P₃ (terminal) = {round(d4,2)} / (0.15−0.07) = {round(p3,2)}
- PV of dividends = {round(pv_d,2)}, PV of terminal = {round(pv_p,2)}
""")

    elif level == "Advanced":
        st.markdown("""
**Problem:** A company has:
- FCFE = ₹800 Cr (growing at 15% for 4 years, then 8% forever)
- Shares outstanding = 200 Cr
- Required return Ke = 16%

Find intrinsic value per share.
""")
        fcfe0 = 800; g1 = 0.15; g2 = 0.08; ke = 0.16; shares = 200
        fcfes = [fcfe0*(1.15)**t for t in range(1,5)]
        pv_f = sum([f/(1.16)**t for t,f in enumerate(fcfes,1)])
        fcfe5 = fcfes[-1]*1.08
        pv_tv = (fcfe5/(0.16-0.08))/(1.16)**4
        total_equity = pv_f + pv_tv
        correct = total_equity / shares

        ans = st.number_input("Your Answer (₹/share)", value=0.0, key="aqb_adv")
        if st.button("Evaluate", key="aqb_adv_btn"):
            if abs(ans - correct) < 2:
                st.success(f"✅ Correct! Intrinsic Value = {currency(correct)}/share")
                st.balloons()
            else:
                st.error(f"❌ Correct Answer = {currency(correct)}/share")

# =========================================================
# PROGRESS TRACKER
# =========================================================

elif menu == "Progress Tracker":

    st.header("📈 Student Progress Tracker")

    if "val_completed" not in st.session_state:
        st.session_state.val_completed = []
    if "val_scores" not in st.session_state:
        st.session_state.val_scores = []

    all_modules = [
        "Bond Basics & Terminology",
        "Bond Valuation",
        "Yield to Maturity (YTM)",
        "Bond Price-Yield Relationship",
        "Duration & Convexity",
        "Types of Bonds",
        "Stock Basics & Terminology",
        "Dividend Discount Model (DDM)",
        "Gordon Growth Model",
        "Multi-Stage DDM",
        "Free Cash Flow to Equity (FCFE)",
        "Price Multiples & Relative Valuation",
        "CAPM & Required Return",
        "Risk Premium & Beta",
    ]

    selected = st.multiselect(
        "Mark completed modules:",
        all_modules,
        default=st.session_state.val_completed
    )
    st.session_state.val_completed = selected

    col1, col2 = st.columns(2)
    with col1:
        quiz_topic = st.selectbox("Quiz Topic", ["Bonds", "DDM", "CAPM", "FCFE", "Multiples"])
    with col2:
        quiz_score = st.number_input("Score (%)", 0, 100, 70)

    if st.button("Log Score"):
        st.session_state.val_scores.append({"topic": quiz_topic, "score": quiz_score})
        st.success("Score logged!")

    st.divider()

    n_done = len(selected)
    n_total = len(all_modules)
    st.metric("Modules Completed", f"{n_done}/{n_total}")
    st.progress(n_done / n_total)

    # Split into bond vs equity
    bond_mods = [m for m in selected if any(k in m for k in ["Bond", "Yield", "Duration", "Types"])]
    equity_mods = [m for m in selected if m not in bond_mods]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Bond Modules", f"{len(bond_mods)}/6")
        st.progress(len(bond_mods)/6)
    with col2:
        st.metric("Equity Modules", f"{len(equity_mods)}/8")
        st.progress(len(equity_mods)/8)

    if st.session_state.val_scores:
        avg = sum(s["score"] for s in st.session_state.val_scores) / len(st.session_state.val_scores)
        st.metric("Average Quiz Score", f"{round(avg,1)}%")
        st.dataframe(pd.DataFrame(st.session_state.val_scores), use_container_width=True)

    if n_done == n_total:
        st.success("🏆 All modules completed! You're ready for the exam.")
        st.balloons()

# =========================================================
# CASE-BASED LEARNING
# =========================================================

elif menu == "Case-Based Learning":

    st.header("📚 Case Study: Valuing Infosys")

    st.markdown("""
## Real-World Valuation Exercise

**Company: Infosys Ltd (INFY)**

You are an equity analyst at a domestic mutual fund. Your task is to value Infosys
using multiple approaches and make a buy/hold/sell recommendation.

**Given Data (FY2024 estimates):**
- EPS: ₹60
- DPS: ₹34 (payout ≈ 57%)
- Book Value per Share: ₹285
- ROE: 31%
- Revenue Growth (5-yr avg): 14%
- Beta: 0.75
- 10-yr G-Sec: 7.2%
- Market Risk Premium: 6%
- Industry P/E: 28x
- Industry P/B: 8x
""")

    st.subheader("Step 1: Required Return (CAPM)")

    rf = 7.2; beta = 0.75; erp = 6.0
    ke = rf + beta * erp
    st.info(f"Ke = {rf} + {beta} × {erp} = **{round(ke,2)}%**")

    st.subheader("Step 2: Sustainable Growth Rate")

    roe = 31.0; payout = 57.0; b = 1 - payout/100
    g = roe * b
    st.info(f"g = ROE × b = {roe} × {round(b,2)} = **{round(g,2)}%**")

    st.subheader("Step 3: Gordon Growth Model")

    d1 = 34 * (1 + g/100)
    if ke > g:
        p_ggm = d1 / ((ke - g)/100)
        st.success(f"D₁ = ₹{round(d1,2)} | P₀ (GGM) = **{currency(p_ggm)}**")
    else:
        st.error("Growth ≥ Ke — GGM not directly applicable")
        p_ggm = None

    st.subheader("Step 4: P/E Relative Valuation")

    pe_val = 60 * 28
    st.success(f"EPS × Industry P/E = 60 × 28 = **{currency(pe_val)}**")

    st.subheader("Step 5: P/B Relative Valuation")

    pb_val = 285 * 8
    st.success(f"BVPS × Industry P/B = 285 × 8 = **{currency(pb_val)}**")

    st.subheader("📊 Valuation Summary")

    vals = {
        "Gordon Growth Model": p_ggm if p_ggm else "N/A",
        "P/E Multiple": pe_val,
        "P/B Multiple": pb_val,
    }

    val_df = pd.DataFrame({
        "Method": list(vals.keys()),
        "Intrinsic Value (₹)": [f"{round(v,0):,.0f}" if isinstance(v, float) else v for v in vals.values()]
    })
    st.table(val_df)

    st.markdown("---")
    st.subheader("Your Recommendation")

    cmp_infy = st.number_input("Enter Current CMP of Infosys (₹)", value=1500.0)

    numeric_vals = [v for v in vals.values() if isinstance(v, float)]
    avg_val = sum(numeric_vals) / len(numeric_vals) if numeric_vals else 0

    st.metric("Average Intrinsic Value", currency(avg_val))
    st.metric("Current Market Price", currency(cmp_infy))

    if avg_val > cmp_infy * 1.1:
        st.success("✅ **BUY** — Stock appears undervalued by >10%")
    elif avg_val < cmp_infy * 0.9:
        st.error("❌ **SELL** — Stock appears overvalued by >10%")
    else:
        st.info("⚖️ **HOLD** — Stock is fairly valued (within ±10%)")
