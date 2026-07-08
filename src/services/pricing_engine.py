# Progressive bulk-bundle discount algorithm logic engine
class PricingEngine:
    MAX_BUNDLE_DISCOUNT = 0.40

    @classmethod
    def compute_sliding_discount(cls, base_total: float, count: int) -> dict:
        discount_percentage = min(0.10 * (count - 1), cls.MAX_BUNDLE_DISCOUNT) if count > 1 else 0.0
        discount_applied = base_total * discount_percentage
        return {
            "base_total": round(base_total, 2),
            "discount_percentage": f"{discount_percentage * 100:.0f}%",
            "discount_applied": round(discount_applied, 2),
            "final_payable": round(base_total - discount_applied, 2)
        }
