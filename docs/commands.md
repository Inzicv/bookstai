# Commandes BookstAI

## Review mock

```powershell
python -m bookstai.cli review --book lesheritiersdorion --opinion "J'ai aimé" --platform tiktok
```

## Review avec HITL

```powershell
python -m bookstai.cli review --book lesheritiersdorion --opinion "J'ai aimé" --platform tiktok --hitl --export json
```

## Song mock

```powershell
python -m bookstai.cli song --book lesheritiersdorion --spoiler-mode spoiler_free --prompt-type thumbnail --platform tiktok --image-backend mock
```

## Song avec HITL

```powershell
python -m bookstai.cli song --book lesheritiersdorion --spoiler-mode spoiler_free --prompt-type thumbnail --platform tiktok --image-backend mock --hitl --export json
```

## HITL show

```powershell
python -m bookstai.cli hitl show --file outputs/hitl/review/lesheritiersdorion.json
```

## HITL edit

```powershell
python -m bookstai.cli hitl edit --file outputs/hitl/review/lesheritiersdorion.json --step review --content "Version corrigée"
```

## Learning extract

```powershell
python -m bookstai.cli learning extract --hitl-file outputs/hitl/review/lesheritiersdorion.json
```

## Learning draft

```powershell
python -m bookstai.cli learning draft --hitl-file outputs/hitl/review/lesheritiersdorion.json
```

## Learning apply

```powershell
python -m bookstai.cli learning apply --draft-file outputs/learning/review/lesheritiersdorion-learning-draft.md --memory-file books/lesheritiersdorion.md
```

## Historique

```powershell
python -m bookstai.cli history tail
```
