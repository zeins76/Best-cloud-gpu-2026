#!/usr/bin/env python3
"""
GPU Cloud Cost Calculator
Quick script to compare total costs across providers

Usage: python cost_calculator.py --hours 47 --gpu rtx5090
"""

import argparse

PROVIDERS = {
    'gpuhub': {
        'rtx5090': 0.36,
        'rtx4090': 0.44,
        'rtx4080s': 0.20,
        'egress': 0.0,
        'storage': 0.0,
        'bonus': 3.0,
        'name': 'GPUhub'
    },
    'runpod': {
        'rtx5090': 0.69,
        'rtx4090': 0.34,
        'rtx4080s': 0.25,
        'egress': 0.09,
        'storage': 0.10,
        'bonus': 2.50,
        'name': 'RunPod'
    },
    'vastai': {
        'rtx5090': 0.35,
        'rtx4090': 0.25,
        'rtx4080s': 0.18,
        'egress': 0.05,
        'storage': 0.05,
        'bonus': 0.0,
        'name': 'Vast.ai'
    },
    'lambda': {
        'rtx5090': 0.55,
        'rtx4090': 0.50,
        'rtx4080s': 0.40,
        'egress': 0.10,
        'storage': 0.20,
        'bonus': 0.0,
        'name': 'Lambda Labs'
    },
    'salad': {
        'rtx5090': 0.45,
        'rtx4090': 0.40,
        'rtx4080s': 0.30,
        'egress': 0.08,
        'storage': 0.10,
        'bonus': 0.0,
        'name': 'SaladCloud'
    }
}

def calculate_cost(provider_key, gpu, hours, storage_gb=50, egress_gb=15):
    p = PROVIDERS[provider_key]
    compute = p[gpu] * hours
    storage = (p['storage'] * storage_gb) * (hours / 720)
    free_egress = 10 if provider_key == 'runpod' else 0
    egress = max(0, (egress_gb - free_egress)) * p['egress']
    total = compute + storage + egress - p['bonus']
    return {
        'provider': p['name'],
        'compute': compute,
        'storage': storage,
        'egress': egress,
        'bonus': p['bonus'],
        'total': max(0, total)
    }

def main():
    parser = argparse.ArgumentParser(description='GPU Cloud Cost Calculator')
    parser.add_argument('--hours', type=float, default=47, help='Hours of usage')
    parser.add_argument('--gpu', choices=['rtx5090', 'rtx4090', 'rtx4080s'], default='rtx5090')
    parser.add_argument('--storage', type=float, default=50, help='Storage in GB')
    parser.add_argument('--egress', type=float, default=15, help='Egress in GB')
    
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"GPU Cloud Cost Comparison")
    print(f"{'='*60}")
    print(f"GPU: {args.gpu.upper()} | Hours: {args.hours} | Storage: {args.storage}GB | Egress: {args.egress}GB")
    print(f"{'='*60}\n")
    
    results = []
    for key in PROVIDERS:
        result = calculate_cost(key, args.gpu, args.hours, args.storage, args.egress)
        results.append(result)
    
    results.sort(key=lambda x: x['total'])
    
    print(f"{'Provider':<15} {'Compute':<10} {'Storage':<10} {'Egress':<10} {'Bonus':<10} {'TOTAL':<10}")
    print(f"{'-'*60}")
    
    for i, r in enumerate(results):
        medal = '🥇' if i == 0 else '🥈' if i == 1 else '🥉' if i == 2 else '  '
        print(f"{medal} {r['provider']:<13} ${r['compute']:<9.2f} ${r['storage']:<9.2f} ${r['egress']:<9.2f} -${r['bonus']:<9.2f} ${r['total']:<9.2f}")
    
    print(f"\n{'='*60}")
    print(f"💡 Best value: {results[0]['provider']} at ${results[0]['total']:.2f}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
