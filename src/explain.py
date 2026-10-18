"""Plain-language explanations built ONLY from verified numbers.
These are TEMPLATE-BASED (fixed sentences), not written by an AI model."""

LABEL = "Explanation built from a fixed template using calculated figures (not AI-written)."
CLOSING = ("This is an unusual change in your records that is worth reviewing. "
           "It does not by itself prove that the platform underpaid you.")


def _peer_sentence(peer):
    if peer is None:
        return "A peer comparison was not calculated for this measure."
    if not peer.get("available"):
        return "Peer comparison hidden: " + peer.get("reason", "not available.")
    return (f"Among {peer['n_peers']} similar workers ({peer['group']}), the same "
            f"measure changed by {peer['peer_pct_change']:+.1f}%.")


def explain_flag(flag, peer=None):
    kind, slot = flag["flag_type"], flag["slot"]
    old, new, ch = flag["earlier"], flag["recent"], flag["pct_change"]
    if kind == "pay_rate_drop":
        main = (f"Your base pay per km in the {slot} slot fell from Rs {old:.2f} "
                f"to Rs {new:.2f}, a change of {ch:.1f}%.")
        peer_text = _peer_sentence(peer)
    elif kind == "deduction_increase":
        main = (f"Deductions took {old * 100:.1f}% of your gross pay in the earlier "
                f"weeks and {new * 100:.1f}% in the recent weeks, a relative rise of {ch:.0f}%.")
        peer_text = _peer_sentence(None)
    else:
        main = (f"Incentives made up {old * 100:.1f}% of your gross pay in the earlier "
                f"weeks and {new * 100:.1f}% in the recent weeks, a change of {ch:.0f}%.")
        peer_text = _peer_sentence(None)
    return " ".join([main, peer_text, CLOSING])
