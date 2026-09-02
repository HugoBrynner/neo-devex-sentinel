# Neo DevEx Sentinel — Release Impact Report

**Release:** `v3.10.0` → `v3.10.1`

**Detected:** 10 developer-facing changes — 0 high / 9 medium / 1 low

## MEDIUM — public_type_added — `AccessControl`

Source: `AccessControl.cs`
- After: `public abstract class AccessControl`
- Exact docs hits: none
- Related docs hits: none
- Note: New public API surface; documentation coverage should be reviewed.

## MEDIUM — public_type_added — `Ownable2Step`

Source: `Ownable2Step.cs`
- After: `public abstract class Ownable2Step`
- Exact docs hits: none
- Related docs hits: none
- Note: New public API surface; documentation coverage should be reviewed.

## MEDIUM — public_type_added — `PausableOwnable`

Source: `PausableOwnable.cs`
- After: `public abstract class PausableOwnable`
- Exact docs hits: none
- Related docs hits: none
- Note: New public API surface; documentation coverage should be reviewed.

## MEDIUM — public_type_added — `RoyaltyNep11Token`

Source: `RoyaltyNep11Token.cs`
- After: `public abstract class RoyaltyNep11Token<TokenState>`
- Exact docs hits: none
- Related docs hits: `nep11.md`
- Note: New public API surface; documentation coverage should be reviewed.

## MEDIUM — public_method_added — `AcceptOwnership`

Source: `Ownable2Step.cs`
- After: `void AcceptOwnership()`
- Exact docs hits: none
- Related docs hits: none

## MEDIUM — public_method_added — `GetOwner`

Source: `Ownable2Step.cs`
- After: `UInt160? GetOwner()`
- Exact docs hits: none
- Related docs hits: none

## MEDIUM — public_method_added — `OnlyRole`

Source: `AccessControl.cs`
- After: `void OnlyRole(int role, UInt160 account)`
- Exact docs hits: none
- Related docs hits: none

## MEDIUM — public_method_added — `Pause`

Source: `PausableOwnable.cs`
- After: `void Pause()`
- Exact docs hits: none
- Related docs hits: none

## LOW — public_method_added — `RoyaltyInfo`

Source: `RoyaltyNep11Token.cs`
- After: `Map<string, object>[] RoyaltyInfo(ByteString tokenId, UInt160 royaltyToken, BigInteger salePrice)`
- Exact docs hits: `nep11.md`
- Related docs hits: none

## MEDIUM — public_method_added — `Unpause`

Source: `PausableOwnable.cs`
- After: `void Unpause()`
- Exact docs hits: none
- Related docs hits: none
