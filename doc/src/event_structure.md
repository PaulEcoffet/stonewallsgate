Structure des fichier event.json
================================

```json
{
    "conditions":
        [
            {
                "test": "nom_du_test",
                "params": ["liste", "de", "params"]
            },
            {
                "test": "vie_sup",
                "params": [30]
            }
        ],
    "dialogue": "ref_dialogue",
    "triggers":
        [
            {
                "trigger": "ajouter_vie",
                "params": [30]
            },
            {
                "trigger": "ajouter_obj",
                "params": ["munitions", 30]
            },
            {
                "trigger": "ajouter_quete",
                "param": "ref_quete"
            }
        ]
}
```
