pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer",
            "description": "The pet ID"
        },
        "name": {
            "type": "string",
            "description": "The pet name"
        },
        "type": {
            "type": "string",
            "description": "The pet type",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "description": "The pet status",
            "enum": ["available", "sold", "pending"]
        }
    }
}

order = {
    "type": "object",
    "required": ["pet_id"],
    "properties": {
        "id": {
            "type": "string",
            "description": "The order ID",
            "readOnly": True
        },
        "pet_id": {
            "type": "integer",
            "description": "The ID of the pet"
        }
    }
}
