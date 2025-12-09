/**
 * Path: client/src/game/Action.ts
 * Purpose: Defines action system for turn-based combat
 * Logic:
 *   - Base Action interface for all combat actions
 *   - Common action implementations (Attack, Dash, etc.)
 *   - Action execution with results
 */

import { CombatEntity } from '../sprites/CombatEntity';

export interface ActionResult {
    success: boolean;
    message: string;
    damage?: number;
    healing?: number;
}

export interface Action {
    name: string;
    description: string;
    shortcut: string; // e.g., "1", "2", etc.
    requiresTarget: boolean;

    /**
     * Check if this action can be used
     */
    canUse(caster: CombatEntity): boolean;

    /**
     * Execute the action
     */
    execute(caster: CombatEntity, target?: CombatEntity): ActionResult;
}

/**
 * Basic melee attack action
 */
export class AttackAction implements Action {
    name = 'Attack';
    description = 'Make a melee attack';
    shortcut = '1';
    requiresTarget = true;

    canUse(caster: CombatEntity): boolean {
        return !caster.getIsDead();
    }

    execute(caster: CombatEntity, target?: CombatEntity): ActionResult {
        if (!target || target.getIsDead()) {
            return {
                success: false,
                message: 'No valid target'
            };
        }

        // Simple attack: d20 + attack bonus
        const attackRoll = this.d20();
        const attackBonus = Math.floor(caster.getStats().attack / 5); // Simplified
        const totalAttack = attackRoll + attackBonus;

        // Target AC = 10 + defense
        const targetAC = 10 + Math.floor(target.getStats().defense);

        if (totalAttack >= targetAC) {
            // Hit! Roll damage
            const damage = this.rollDamage(caster);
            target.takeDamage(damage);

            return {
                success: true,
                message: `Hit! (${attackRoll}+${attackBonus} vs AC ${targetAC})`,
                damage
            };
        } else {
            return {
                success: false,
                message: `Miss! (${attackRoll}+${attackBonus} vs AC ${targetAC})`
            };
        }
    }

    private d20(): number {
        return Math.floor(Math.random() * 20) + 1;
    }

    private rollDamage(caster: CombatEntity): number {
        // 1d8 + attack modifier
        const die = Math.floor(Math.random() * 8) + 1;
        const modifier = Math.floor(caster.getStats().attack / 10);
        return die + modifier;
    }
}

/**
 * Dash action - doubles movement speed
 */
export class DashAction implements Action {
    name = 'Dash';
    description = 'Double your movement speed this turn';
    shortcut = '2';
    requiresTarget = false;

    canUse(caster: CombatEntity): boolean {
        return !caster.getIsDead();
    }

    execute(_caster: CombatEntity): ActionResult {
        // This would need integration with TurnManager to actually double movement
        return {
            success: true,
            message: 'Movement speed doubled!'
        };
    }
}

/**
 * Dodge action - makes you harder to hit
 */
export class DodgeAction implements Action {
    name = 'Dodge';
    description = 'Enemies have disadvantage to hit you';
    shortcut = '3';
    requiresTarget = false;

    canUse(caster: CombatEntity): boolean {
        return !caster.getIsDead();
    }

    execute(_caster: CombatEntity): ActionResult {
        // Would need to add "dodging" status effect
        return {
            success: true,
            message: 'You take a defensive stance!'
        };
    }
}

/**
 * Pass action - do nothing
 */
export class PassAction implements Action {
    name = 'Pass';
    description = 'End your turn without acting';
    shortcut = '0';
    requiresTarget = false;

    canUse(_caster: CombatEntity): boolean {
        return true;
    }

    execute(_caster: CombatEntity): ActionResult {
        return {
            success: true,
            message: 'Turn ended'
        };
    }
}
